# SmartHome AI Monitor — Workflow Complet (A → Z)

> **Document de référence — Module IoT ENSA FES**  
> Pr. Balboul Younes

---

## 1. La Problématique Réelle

### Contexte
Imaginez une **salle serveur** dans une école, un **local électrique** dans un immeuble, ou une **chambre médicale** dans une clinique. Ces espaces ont en commun un besoin critique : être surveillés en permanence, même quand personne n'est présent physiquement.

**Les risques concrets :**
| Risque | Déclencheur | Conséquence |
|--------|-------------|-------------|
| Incendie | Température > 35°C | Perte de données / vies |
| Surchauffe équipement | Humidité < 30% + T° élevée | Panne serveur / court-circuit |
| Moisissures / corrosion | Humidité > 80% pendant longtemps | Dégradation du matériel |
| Panne climatisation | Montée progressive T° sur 1h | Arrêt d'activité |

### Ce que ce projet résout
Ce système remplace un **gardien humain 24h/24** par une infrastructure IoT intelligente qui :
- Collecte les données **toutes les 3 secondes**
- Détecte automatiquement les **anomalies statistiques** (Z-Score > 2.5)
- **Prédit** l'évolution de la température dans les 5 prochaines minutes
- **Commande à distance** les relais (climatiseur, ventilateur, alarme lumineuse)
- Envoie des **alertes en temps réel** via le dashboard web

---

## 2. Architecture Complète (A → Z)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  COUCHE CAPTEURS (Edge Device)                                          │
│                                                                         │
│  ┌─────────────────────────┐                                            │
│  │  ESP32 (Wokwi VS Code)  │                                            │
│  │  ou mock_esp.py (Docker)│                                            │
│  │                         │                                            │
│  │  ┌──────────┐           │                                            │
│  │  │  DHT22   │ T°, Hum   │                                            │
│  │  └──────────┘           │                                            │
│  │  ┌──────────┐           │                                            │
│  │  │ Relais 1 │ Broche 2  │  ← Climatiseur / Ventilateur              │
│  │  └──────────┘           │                                            │
│  │  ┌──────────┐           │                                            │
│  │  │ Relais 2 │ Broche 4  │  ← Alarme lumineuse / Pompe              │
│  │  └──────────┘           │                                            │
│  └────────────┬────────────┘                                            │
│               │ MQTT QoS 0 (TCP 1883) ou QoS 2 (tests)                 │
└───────────────┼─────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  COUCHE TRANSPORT (Broker MQTT Public)                                  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    broker.emqx.io                              │    │
│  │                                                                │    │
│  │  Port 1883  → MQTT TCP standard (ESP32 / mock_esp)            │    │
│  │  Port 8883  → MQTT TLS/SSL (production sécurisée)             │    │
│  │  Port 8083  → MQTT WebSocket (Dashboard navigateur)           │    │
│  │  Port 8084  → MQTT WebSocket TLS (prod navigateur)            │    │
│  │                                                                │    │
│  │  Topics utilisés :                                             │    │
│  │  ├── home/wokwi/sensors/dht        (publish ESP32)            │    │
│  │  ├── home/wokwi/relay1/command     (subscribe ESP32)          │    │
│  │  ├── home/wokwi/relay2/command     (subscribe ESP32)          │    │
│  │  ├── home/wokwi/relay1/status      (publish ESP32 confirmé)   │    │
│  │  ├── home/wokwi/relay2/status      (publish ESP32 confirmé)   │    │
│  │  ├── home/wokwi/ai/anomaly         (publish Node-RED/IA)      │    │
│  │  └── home/wokwi/ai/prediction      (publish Node-RED/IA)      │    │
│  └────────────────────────────────────────────────────────────────┘    │
│               │                          │                              │
└───────────────┼──────────────────────────┼──────────────────────────────┘
                │                          │
        ┌───────┘                          └────────────┐
        ▼                                               ▼
┌────────────────────────┐              ┌───────────────────────────┐
│  Node-RED (:1880)      │              │  Dashboard Web (:8080)    │
│  [Orchestrateur]       │ ──MQTT──▶   │  [Interface Utilisateur]  │
│                        │             │                            │
│  ► SmartHome Monitor   │             │  - Température / Humidité │
│  ► Automation & Alerte │             │  - Graphique temps réel   │
│  ► Debug & QoS         │             │  - Prédiction IA 5 min    │
│                        │             │  - Contrôle relais        │
│         │              │             │  - Système d'alarme       │
│         │ HTTP POST    │             └───────────────────────────┘
│         ▼              │
│  ┌──────────────────┐  │
│  │  AI Server (:5000│  │
│  │  [Python Flask]  │  │
│  │                  │  │
│  │  - Z-Score       │  │
│  │  - Régression    │  │
│  │    linéaire      │  │
│  └──────────────────┘  │
└────────────────────────┘
```

---

## 3. Les Protocoles de Communication

### MQTT — Message Queuing Telemetry Transport
**Pourquoi MQTT et pas HTTP ?**

HTTP fonctionne en mode "demande → réponse". Pour avoir des données en temps réel, il faudrait que le dashboard interroge le serveur toutes les secondes (polling). Cela génère des milliers de requêtes inutiles et un délai de 1 seconde minimum.

MQTT fonctionne en mode **Publication/Abonnement** (Pub/Sub). Le capteur publie une donnée UNE fois, et TOUS les abonnés (dashboard, Node-RED, mobile...) la reçoivent **instantanément**, sans demander.

| Critère | HTTP | MQTT |
|---------|------|------|
| Latence | ~1000ms (polling) | ~50ms (push) |
| Bande passante | Elevée (headers HTTP) | Ultra faible (2 bytes header) |
| Connexions simultanées | Complexe | Natif |
| Idéal pour IoT | Non | Oui |

### Les Niveaux QoS (Quality of Service)
| QoS | Nom | Garantie | Usage dans ce projet |
|-----|-----|---------|----------------------|
| 0 | At most once | Message peut se perdre | Données capteurs (temperature) |
| 1 | At least once | Message reçu au moins 1x | Commandes relais |
| 2 | Exactly once | Message reçu exactement 1x | Tests / alarmes critiques |

### WebSocket — Pour le Dashboard Navigateur
Un navigateur web ne peut pas ouvrir une connexion TCP brute (sécurité). WebSocket est un protocole HTTP "upgradé" qui crée un tunnel bi-directionnel persistent. Le broker EMQX expose le port 8083 pour accepter les connexions MQTT-over-WebSocket depuis le dashboard.

### TLS/SSL — Pour la Production
Sur les ports 8883 (MQTT) et 8084 (WebSocket), le broker chiffre les données. En production réelle, on utilise un **certificat client** pour s'assurer que seul votre ESP32 peut publier des données (authentification mutuelle).

---

## 4. Explication des Sections Node-RED

### Flux 1 : "SmartHome Monitor" (Collecte des données)
```
[MQTT IN: home/wokwi/sensors/dht]
           │
           ▼
    [JSON Parse]          ← Convertit le texte brut en objet JavaScript
           │
    ┌──────┴──────┐
    ▼             ▼
[HTTP POST     [MQTT OUT]
 → AI Server]  → home/wokwi/sensors/processed
    │
    ▼
[JSON Parse]
    │
    ├─→ [MQTT OUT: home/wokwi/ai/anomaly]
    └─→ [MQTT OUT: home/wokwi/ai/prediction]
```
**Rôle :** Recevoir les données brutes de l'ESP32, les envoyer à l'intelligence artificielle Python, et redistribuer les résultats analysés à tous les abonnés.

### Flux 2 : "Automation & Alertes" (Automatisation)
```
[MQTT IN: home/wokwi/ai/anomaly]
           │
           ▼
   [Switch: anomaly == true ?]
           │
     ┌─────┴──────┐
     ▼             ▼
[Relais 1 ON]  [Notification]
 (climatiseur)
```
**Rôle :** Déclencher automatiquement des actions quand l'IA détecte un problème. Si la température dépasse le seuil, le climatiseur (Relais 1) s'active SANS intervention humaine. C'est ce qui rend le système autonome.

### Flux 3 : "Debug & QoS" (Tests et Diagnostics)
Ce flux contient des nœuds de test QoS 2 qui permettent de valider que les messages critiques arrivent exactement une fois. Il contient aussi des nœuds `debug` pour visualiser en temps réel les messages qui circulent dans le système, indispensables pour le débogage.

---

## 5. Explication des Sections EMQX (Broker Local)

### Monitoring
4 tableaux de bord clés :
- **Connexions actives** : combien d'appareils sont connectés en ce moment
- **Messages/seconde** : débit du broker (permet de détecter une surcharge)
- **Topics actifs** : liste tous les canaux de communication ouverts
- **Rétention mémoire** : messages mis en cache pour les clients hors-ligne

### Access Control
Protection du broker contre les accès non autorisés :
- **Authentification** : identifiant/mot de passe pour chaque client (CLIENT1/CLIENT123)
- **ACL (Access Control List)** : définit qui peut publier et qui peut s'abonner à quel topic
- Exemple : seul l'ESP32 peut publier sur `home/wokwi/sensors/dht`, le dashboard peut seulement lire

### Integration
Connexion du broker EMQX avec des services externes :
- **Webhook** : envoyer une alerte HTTP à un serveur externe lors d'un événement
- **Data Bridge** : répliquer les données vers une base de données (InfluxDB, TimescaleDB)
- Dans notre projet : le bridge HTTP vers le AI Server Python

### Management
Administration du broker :
- **Clients** : voir et déconnecter des clients
- **Subscriptions** : lister tous les abonnements actifs
- **Plugins** : activer/désactiver des fonctionnalités
- **Configuration à chaud** : modifier les paramètres sans redémarrage

### Diagnose
Outils de débogage réseau :
- **Log en temps réel** : voir chaque message qui passe par le broker
- **WebSocket Test** : tester une connexion MQTT depuis l'interface web du broker
- **Topic inspector** : espionner tous les messages d'un topic spécifique

---

## 6. Rôle des 2 Relais — Pourquoi c'est pertinent

### Relais 1 — LED Rouge (GPIO 2) → Climatiseur / Ventilateur
Quand la température dépasse 30°C, l'automation Node-RED envoie automatiquement `{"state": "ON"}` sur `home/wokwi/relay1/command`. Cela simule l'activation d'un climatiseur ou d'un ventilateur industriel pour refroidir la salle.

**En production réelle :** Le relais physique (module 5V) commute une charge 220V (climatiseur réel) via un optocoupleur qui isole électriquement le microcontrôleur de la puissance.

### Relais 2 — LED Verte (GPIO 4) → Alarme lumineuse / Pompe
Quand l'humidité dépasse 80% (risque de dégâts des eaux) ou quand une anomalie critique est détectée, le Relais 2 s'active. Cela peut simuler une sirène d'alarme lumineuse ou une pompe de drainage.

**La boucle de confirmation :**
```
Dashboard ──MQTT──▶ relay1/command ──▶ ESP32 ──▶ actionne relais
                                                    │
Dashboard ◀──MQTT── relay1/status  ◀──────────────┘
```
L'ESP32 publie `relay1/status` après chaque action pour confirmer au dashboard l'état réel du relais (et non l'état désiré). C'est le principe du **feedback d'état** qui évite les désynchronisations.

---

## 7. Problèmes Techniques Rencontrés et Solutions

### Problème 1 : Wokwi VS Code — Boucle de redémarrage infinie
**Symptôme :** `rst:0x3 (SW_RESET)` en boucle dans le terminal Wokwi.  
**Cause :** L'extension VS Code de Wokwi pour MicroPython nécessite un firmware `.bin` pré-compilé. Elle ne peut pas exécuter `main.py` directement sans ce firmware. Quand elle essaie, l'ESP32 plante au boot car il reçoit du texte Python au lieu de bytecode.  
**Solution :** Télécharger le firmware MicroPython officiel (`micropython.bin`) et le référencer dans `wokwi.toml`, puis utiliser `mpremote` pour injecter `main.py` via le port RFC2217 (port 4000 configuré dans `wokwi.toml`).

### Problème 2 : Docker Windows — Erreur EBUSY sur flows.json
**Symptôme :** `Deploy failed: EBUSY resource busy or locked`.  
**Cause :** Sur Windows avec Docker Desktop (WSL2), les fichiers montés via bind-mount (`./flows.json:/data/flows.json`) sont verrouillés par Windows Explorer/VS Code, et Node-RED ne peut pas les réécrire atomiquement (la réécriture atomique requiert un `rename()` qui échoue sur le filesystem partagé Windows-Linux).  
**Solution :** Utiliser un **volume Docker nommé** (`nodered_data:/data`) géré par Docker dans l'espace Linux pur, et copier le `flows.json` initial dedans via la commande Docker.

### Problème 3 : paho-mqtt Version 1 vs Version 2
**Symptôme :** `TypeError: on_connect() takes 4 positional arguments but 5 were given`.  
**Cause :** paho-mqtt v2.x a ajouté un paramètre `properties` dans tous les callbacks ET a rendu obligatoire l'utilisation de `CallbackAPIVersion`.  
**Solution :** Détection automatique avec `try/except ImportError` pour supporter les deux versions.

### Problème 4 : Données statiques non représentatives
**Symptôme :** La température affichée reste autour de 24°C ±2 de façon aléatoire uniforme, sans tendance.  
**Solution :** Simuler une courbe sinusoïdale journalière (plus chaud l'après-midi, montée progressive des anomalies).

---

## 8. Comment Utiliser le Système (Guide de démarrage)

### Démarrage Complet
```batch
# Étape 1 : Lancer tous les services Docker
start.bat

# Étape 2 : Ouvrir le dashboard
http://localhost:8080

# Étape 3 : Ouvrir Node-RED (si besoin d'ajustements)
http://localhost:1880

# Étape 4A : Lancer le simulateur automatique (sans Wokwi)
# → Automatique via Docker (esp_simulator)

# Étape 4B : Lancer Wokwi VS Code
# → Ouvrir diagram.json → Play → puis : .\run_wokwi_code.bat
```

### Test MQTTX (Validation Communication)
```
1. Ouvrir MQTTX (app.mqttx.org ou application desktop)
2. Nouvelle connexion :
   - Host : broker.emqx.io
   - Port : 8083 (WebSocket) ou 1883 (TCP)
   - Client ID : mqttx_test_001
3. S'abonner à : home/wokwi/sensors/dht
4. Observer les données en temps réel
5. Publier sur home/wokwi/relay1/command :
   {"relay": "relais1", "state": "ON"}
6. Vérifier que la LED du simulateur Wokwi s'allume
```

### Test TLS (Production)
```
Connexion sécurisée via port 8883 :
- Activer "SSL/TLS" dans MQTTX
- Désactiver "Verify Server Certificate" (certificat public EMQX)
- Même fonctionnement qu'en clair, mais chiffré end-to-end
```

---

*Généré automatiquement — SmartHome AI Monitor — ENSA FES 2026*
