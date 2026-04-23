# 📌 Contraintes et Exigences du Projet

> Ce document mémorise les règles imposées par le professeur et justifie comment notre projet les respecte.

---

## ✅ Outils Autorisés — Conformité du Projet

| Outil Autorisé | Ce que Nous Utilisons | Conformité |
|---|---|---|
| **Wokwi** (simulation ESP32) | `wokwi_main.py` + `wokwi_diagram.json` — Simule un ESP32 avec capteur DHT22 et LED/Relais | ✅ |
| **Broker MQTT public ou cloud** | `broker.emqx.io` (broker public gratuit, standard IoT industriel) | ✅ |
| **Node-RED local ou cloud** | Node-RED installé localement (Windows natif) — Flux d'orchestration dans `flows.json` | ✅ |
| **API web simulée ou réelle (HTTP/HTTPS)** | `ai_server.py` — Serveur Flask (Python) exposant une vraie API REST sur `http://127.0.0.1:5000/predict` et `/status` | ✅ |

---

## 🏗 Architecture du Projet

```
┌─────────────────────────────────────────────────────────┐
│                       CLOUD PUBLIC                       │
│              broker.emqx.io  (Port 1883/8083)           │
└────────────────┬────────────────────────────────────────┘
                 │  Protocole MQTT
    ┌────────────┴──────────────────┐
    │                               │
    ▼                               ▼
┌──────────────────┐     ┌──────────────────────────────┐
│  Wokwi (ESP32)   │     │     PC Local (Windows)        │
│  Simulation en   │     │                              │
│  ligne (navigat) │     │  ┌─────────┐  ┌──────────┐  │
│                  │     │  │Node-RED │→ │IA Python │  │
│ - DHT22 capteur  │     │  │(Port    │  │(Flask)   │  │
│ - LED relais     │     │  │ 1880)   │  │Port 5000 │  │
│ - MicroPython    │     │  └─────────┘  └──────────┘  │
└──────────────────┘     │                              │
                         │  ┌─────────────────────────┐ │
                         │  │ Dashboard HTML             │ │
                         │  │ (browser + MQTT WebSocket)│ │
                         │  │ Port 8080                 │ │
                         │  └─────────────────────────┘ │
                         └──────────────────────────────┘
```

---

## ✅ Critères de Validation — Conformité

### 1. Démonstration Fonctionnelle
- L'ESP32 simulé (Wokwi) publie des données réelles de température et d'humidité.
- Le Dashboard Web se met à jour en temps réel avec ces données.
- Le relais (LED) dans Wokwi réagit aux commandes envoyées depuis le Dashboard.
- L'IA Python détecte les anomalies et prédit la température future.

### 2. Architecture Claire
- Protocoles : **MQTT** (IoT) et **HTTP REST** (IA).
- Séparation des responsabilités : Wokwi gère le matériel, Node-RED l'orchestration, Python l'intelligence, HTML la visualisation.

### 3. Choix Techniques Justifiés
- **Wokwi** : Pas besoin de matériel physique. Simulation fidèle et gratuite.
- **broker.emqx.io** : Standard de l'industrie IoT. Disponible 24h/24 sans installation.
- **Node-RED** : Outil professionnel dédié à l'IoT, orchestration visuelle.
- **Flask (Python)** : API légère pour l'IA — détection d'anomalies (Z-Score) + prédiction (Régression linéaire).
- **MQTT WebSocket** : Mise à jour du Dashboard en temps réel sans rechargement de la page.

### 4. Travail Personnel Visible
- Code MicroPython (`wokwi_main.py`) écrit sur mesure.
- Algorithme d'IA (`ai_server.py`) implémenté from scratch avec scikit-learn.
- Flux Node-RED (`flows.json`) créés manuellement nœud par nœud.
- Dashboard HTML complet (`dashboard.html`) avec design moderne (glassmorphism, Chart.js).

---

## 🔗 Topics MQTT Utilisés

| Sujet (Topic) | Direction | Description |
|---|---|---|
| `home/wokwi/sensors/dht` | Wokwi → Cloud → Tout | Données capteur DHT22 (température & humidité) |
| `home/wokwi/ai/anomaly` | Node-RED → Cloud → Dashboard | Résultat d'anomalie détectée par l'IA |
| `home/wokwi/ai/prediction` | Node-RED → Cloud → Dashboard | Prédiction de température dans 5 minutes |
| `home/wokwi/relay/command` | Dashboard → Cloud → Wokwi | Commande ON/OFF pour le relais |
| `home/wokwi/relay/status` | Wokwi → Cloud → Dashboard | Confirmation de l'état du relais |

---

## ▶ Comment Lancer le Projet

1. Lancer **`start_local.bat`** (Lance Node-RED, IA Python, Serveur Web)
2. Aller sur **[Wokwi]( https://wokwi.com/)** → Créer un projet MicroPython ESP32
3. Coller le contenu de **`wokwi_diagram.json`** dans l'onglet `diagram.json` de Wokwi
4. Coller le contenu de **`wokwi_main.py`** dans l'onglet `main.py` de Wokwi
5. Lancer la simulation Wokwi ▶
6. Observer les données en direct sur **`http://127.0.0.1:8080/dashboard.html`**
7. Optionnel : Ouvrir **MQTTX** → Connecter sur `broker.emqx.io:1883` → S'abonner à `home/wokwi/#`
