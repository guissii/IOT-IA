import network
import time
import json
import dht
from umqtt.simple import MQTTClient
from machine import Pin

# ─── Configuration Réseau et MQTT ─────────────────────────────────────────────
WIFI_SSID = 'Wokwi-GUEST'
WIFI_PASS = ''

MQTT_BROKER = 'broker.emqx.io'   # Broker public accessible depuis Wokwi
MQTT_PORT   = 1883
CLIENT_ID   = 'esp32_wokwi_ensa_tp2'

# Topics
TOPIC_DHT     = b"home/wokwi/sensors/dht"
TOPIC_RELAY1  = b"home/wokwi/relay1/command"
TOPIC_RELAY2  = b"home/wokwi/relay2/command"
TOPIC_STATUS1 = b"home/wokwi/relay1/status"
TOPIC_STATUS2 = b"home/wokwi/relay2/status"

# ─── Matériel (ESP32 + DHT22 + 2 Relais) ────────────────────────────────────
dht_sensor = dht.DHT22(Pin(15))
relay1_pin  = Pin(2, Pin.OUT)
relay2_pin  = Pin(4, Pin.OUT)
relay1_pin.value(0)
relay2_pin.value(0)

# Variables d'état des relais
global_relay1_state = "OFF"
global_relay2_state = "OFF"

# ─── Connexion WiFi ──────────────────────────────────────────────────────────
def connect_wifi():
    print("[WIFI] Connexion", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASS)
    timeout = 0
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.5)
        timeout += 1
        if timeout > 20:
            print("\n[WIFI] ECHEC — timeout")
            return False
    print("\n[WIFI] Connecté! IP:", sta_if.ifconfig()[0])
    return True

# ─── Callback MQTT (réception des commandes) ────────────────────────────────
def mqtt_callback(topic, msg):
    global global_relay1_state, global_relay2_state
    print(f"\n[MQTT] Commande reçue sur '{topic.decode()}' : {msg.decode()}")
    try:
        data = json.loads(msg.decode())
        state_val = data.get("state", "").upper()

        if topic == TOPIC_RELAY1:
            relay1_pin.value(1 if state_val == "ON" else 0)
            global_relay1_state = state_val
            print(f"[RELAIS 1] → {'ACTIVÉ' if state_val=='ON' else 'DÉSACTIVÉ'}")
            client.publish(TOPIC_STATUS1, json.dumps({
                "relay": "relais1",
                "state": global_relay1_state
            }))

        elif topic == TOPIC_RELAY2:
            relay2_pin.value(1 if state_val == "ON" else 0)
            global_relay2_state = state_val
            print(f"[RELAIS 2] → {'ACTIVÉ' if state_val=='ON' else 'DÉSACTIVÉ'}")
            client.publish(TOPIC_STATUS2, json.dumps({
                "relay": "relais2",
                "state": global_relay2_state
            }))

    except Exception as e:
        print("[ERREUR] Parsing JSON:", e)

# ─── Démarrage avec gestion d'erreurs robuste ────────────────────────────────
print("\n========================================")
print("  SmartHome ESP32 — ENSA FES")
print("========================================\n")

if not connect_wifi():
    print("[FATAL] Pas de WiFi. Redémarrage dans 5s...")
    time.sleep(5)
    import machine
    machine.reset()

# Connexion MQTT avec retry
client = None
for attempt in range(5):
    try:
        print(f"[MQTT] Tentative {attempt+1}/5 → {MQTT_BROKER}:{MQTT_PORT}...")
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.set_callback(mqtt_callback)
        client.connect()
        print("[MQTT] Connecté!\n")
        break
    except Exception as e:
        print(f"[MQTT] Echec: {e}")
        time.sleep(2)

if client is None:
    print("[FATAL] Impossible de se connecter au broker MQTT.")
    print("[FATAL] Redémarrage dans 10s...")
    time.sleep(10)
    import machine
    machine.reset()

# Souscription aux commandes relais
client.subscribe(TOPIC_RELAY1)
client.subscribe(TOPIC_RELAY2)
print(f"[MQTT] Abonné à :\n  → {TOPIC_RELAY1.decode()}\n  → {TOPIC_RELAY2.decode()}")

# ─── Boucle Principale ───────────────────────────────────────────────────────
last_publish = time.ticks_ms()
reading_num  = 0

print("\n[SIM] Simulation directe démarrée. Valeurs interactives Wokwi pures...\n")

try:
    while True:
        client.check_msg()

        if time.ticks_diff(time.ticks_ms(), last_publish) > 5000:
            last_publish = time.ticks_ms()
            reading_num += 1

            try:
                dht_sensor.measure()
                base_t = dht_sensor.temperature()
                base_h = dht_sensor.humidity()

                payload = json.dumps({
                    "temperature": round(base_t, 1),
                    "humidity":    round(base_h, 1),
                    "relay1":      global_relay1_state,
                    "relay2":      global_relay2_state
                })
                client.publish(TOPIC_DHT, payload)
                
                print(f"[PUB #{reading_num:3d}] [Direct] {TOPIC_DHT.decode()} → {payload}")

            except OSError:
                print("[ERREUR] Lecture DHT22 échouée.")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n[SIM] Arrêt propre...")
    relay1_pin.value(0)
    relay2_pin.value(0)
    client.disconnect()
except Exception as e:
    print(f"[ERREUR FATALE] {e}")
    time.sleep(5)
    import machine
    machine.reset()
