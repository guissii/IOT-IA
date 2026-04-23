import time
import json
import random
import math
import os
import sys

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("[ERREUR] paho-mqtt non installé.")
    sys.exit(1)

# ─── Configuration MQTT ──────────────────────────────────────────────────────
MQTT_BROKER = os.environ.get("MQTT_BROKER", "broker.emqx.io")
MQTT_PORT   = int(os.environ.get("MQTT_PORT", 1883))
CLIENT_ID   = "mock_esp32_smarthome_001"

TOPIC_DHT     = "home/wokwi/sensors/dht"
TOPIC_RELAY1  = "home/wokwi/relay1/command"
TOPIC_RELAY2  = "home/wokwi/relay2/command"
TOPIC_STATUS1 = "home/wokwi/relay1/status"
TOPIC_STATUS2 = "home/wokwi/relay2/status"

relay1_state = "OFF"
relay2_state = "OFF"

# ─── Simulation réaliste ─────────────────────────────────────────────────────
# La température suit une courbe sinusoïdale journalière :
# → Minimum ~20°C à 6h du matin
# → Maximum ~28°C à 15h l'après-midi
# + bruit gaussien ±0.4°C pour simuler les fluctuations naturelles
# + anomalies progressives (montée sur 3 mesures, pas instantanées)

start_time     = time.time()
anomaly_phase  = 0    # 0=normal, 1,2,3=montée, 4,5=pic, 6,7=descente
anomaly_cycle  = 0    # compte les mesures depuis la dernière anomalie
ANOMALY_EVERY  = 20   # déclencher une anomalie tous les ~20 mesures

def get_base_temperature():
    """Courbe journalière sinusoïdale : min 20°C, max 28°C."""
    # Utilise l'heure réelle du système
    hour = (time.localtime().tm_hour + time.localtime().tm_min / 60.0)
    # Sinusoïde : pic à 15h, creux à 3h
    angle = (hour - 3) / 24.0 * 2 * math.pi
    return 24.0 + 4.0 * math.sin(angle)

def get_base_humidity(temp):
    """L'humidité est inversement liée à la température (loi naturelle)."""
    # Plus il fait chaud, plus l'humidité relative baisse
    return max(30.0, min(75.0, 70.0 - (temp - 20.0) * 1.5))

def simulate_reading(anomaly_phase):
    """Retourne (temp, hum, is_anomaly) selon la phase d'anomalie."""
    base_temp = get_base_temperature()
    base_hum  = get_base_humidity(base_temp)

    if anomaly_phase == 0:
        # Lecture normale avec bruit naturel
        temp = base_temp + random.gauss(0, 0.4)
        hum  = base_hum  + random.gauss(0, 1.2)
        is_anomaly = False
    elif anomaly_phase == 1:
        # Début de montée (surchauffe progressive)
        temp = base_temp + 2.0 + random.gauss(0, 0.3)
        hum  = base_hum - 5.0  + random.gauss(0, 1.0)
        is_anomaly = False
    elif anomaly_phase == 2:
        temp = base_temp + 5.0 + random.gauss(0, 0.4)
        hum  = base_hum - 10.0 + random.gauss(0, 1.0)
        is_anomaly = True
    elif anomaly_phase == 3:
        temp = base_temp + 8.5 + random.gauss(0, 0.5)
        hum  = base_hum - 15.0 + random.gauss(0, 1.2)
        is_anomaly = True
    elif anomaly_phase in [4, 5]:
        # Pic d'anomalie
        temp = base_temp + random.uniform(10, 14) + random.gauss(0, 0.6)
        hum  = base_hum - 20.0 + random.gauss(0, 1.5)
        is_anomaly = True
    elif anomaly_phase == 6:
        # Descente (le climatiseur (relais1) a réagi)
        temp = base_temp + 5.0 + random.gauss(0, 0.5)
        hum  = base_hum - 8.0  + random.gauss(0, 1.0)
        is_anomaly = True
    else:
        # Retour à la normale
        temp = base_temp + 1.5 + random.gauss(0, 0.4)
        hum  = base_hum - 2.0  + random.gauss(0, 1.0)
        is_anomaly = False

    # Limites physiques réalistes
    temp = round(max(18.0, min(50.0, temp)), 1)
    hum  = round(max(15.0, min(95.0, hum)), 1)
    return temp, hum, is_anomaly

# ─── Callbacks MQTT ──────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[MQTT] Connecte au broker ({MQTT_BROKER}:{MQTT_PORT})")
        client.subscribe(TOPIC_RELAY1)
        client.subscribe(TOPIC_RELAY2)
        print(f"[MQTT] Abonne a :\n  -> {TOPIC_RELAY1}\n  -> {TOPIC_RELAY2}")
    else:
        print(f"[MQTT] Connexion echouee (code={rc})")

def on_message(client, userdata, msg):
    global relay1_state, relay2_state
    try:
        data  = json.loads(msg.payload.decode())
        state = data.get("state", "").upper()
        if msg.topic == TOPIC_RELAY1:
            relay1_state = state
            print(f"[RELAIS 1] -> {state}")
            client.publish(TOPIC_STATUS1, json.dumps({"relay": "relais1", "state": relay1_state}), qos=1)
        elif msg.topic == TOPIC_RELAY2:
            relay2_state = state
            print(f"[RELAIS 2] -> {state}")
            client.publish(TOPIC_STATUS2, json.dumps({"relay": "relais2", "state": relay2_state}), qos=1)
    except Exception as e:
        print(f"[ERREUR] Parsing commande : {e}")

def on_disconnect(client, userdata, rc, properties=None):
    print(f"[MQTT] Deconnecte (code={rc}). Reconnexion en cours...")

# ─── Initialisation Client MQTT ──────────────────────────────────────────────
try:
    from paho.mqtt.enums import CallbackAPIVersion
    client = mqtt.Client(CallbackAPIVersion.VERSION1, client_id=CLIENT_ID)
    print("[INFO] paho-mqtt v2 detecte")
except (ImportError, AttributeError, TypeError):
    client = mqtt.Client(client_id=CLIENT_ID)
    print("[INFO] paho-mqtt v1 detecte")

client.on_connect    = on_connect
client.on_message    = on_message
client.on_disconnect = on_disconnect

print(f"[SIM] Connexion a {MQTT_BROKER}:{MQTT_PORT}...")
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()

# ─── Boucle de simulation ─────────────────────────────────────────────────────
reading_num   = 0
anomaly_cycle = 0
anomaly_phase = 0
ANOMALY_EVERY = 20

print("[SIM] Simulation ESP32 demarre — courbe journaliere realiste, publication toutes les 3s...")
print(f"[SIM] Heure locale : {time.strftime('%H:%M:%S')}")

try:
    while True:
        reading_num   += 1
        anomaly_cycle += 1

        # Déclenchement d'une séquence d'anomalie tous les ANOMALY_EVERY mesures
        if anomaly_cycle >= ANOMALY_EVERY and anomaly_phase == 0:
            anomaly_phase = 1
            anomaly_cycle = 0
            print(f"\n[SIM] *** DEBUT SEQUENCE ANOMALIE ***")

        temp, hum, is_anomaly = simulate_reading(anomaly_phase)

        # Avancement de la phase d'anomalie
        if anomaly_phase > 0:
            anomaly_phase += 1
            if anomaly_phase > 7:
                anomaly_phase = 0
                print(f"[SIM] *** FIN SEQUENCE ANOMALIE — retour a la normale ***\n")

        status = "** ANOMALIE **" if is_anomaly else "Normal"
        base   = get_base_temperature()
        print(f"[SIM #{reading_num:4d}] {status:15s} | T={temp:5.1f}°C (base={base:.1f}) | H={hum:4.1f}% | R1={relay1_state} R2={relay2_state}")

        payload = json.dumps({
            "temperature": temp,
            "humidity"   : hum,
            "relay1"     : relay1_state,
            "relay2"     : relay2_state
        })

        result = client.publish(TOPIC_DHT, payload, qos=0)
        if result.rc != 0:
            print(f"[ERREUR] Publication echouee (rc={result.rc})")

        time.sleep(3)

except KeyboardInterrupt:
    print("\n[SIM] Arret propre...")
    client.loop_stop()
    client.disconnect()
