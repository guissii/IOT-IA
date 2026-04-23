# Guide Complet de Dépannage (Troubleshooting) - SmartHome Monitor

Ce fichier recense tous les problèmes potentiels pouvant survenir lors du déploiement, de l'exécution ou du développement du système IoT **SmartHome Monitor**, ainsi que leurs solutions détaillées. Il sert de manuel technique de référence pour garantir la robustesse du système lors des présentations.

---

## 1. Problèmes liés à l'Infrastructure et Docker

### 1.1. Erreur de connexion au démon Docker (Docker non démarré)
* **Symptômes** : Lors de l'exécution de `start.bat`, l'erreur `error during connect: open //./pipe/docker_engine` s'affiche.
* **Cause** : Docker Desktop n'est pas lancé, ou le sous-système Windows pour Linux (WSL2) a crashé.
* **Solution** : 
  1. Ouvrir Docker Desktop manuellement.
  2. Si bloqué sur "Starting the Docker Engine", redémarrer le système Windows (cela réinitialise les interfaces Hyper-V et WSL2).
  3. Si le problème persiste, forcer l'arrêt via PowerShell : `wsl --shutdown` puis relancer Docker Desktop.

### 1.2. Conflit de ports (Ports déjà utilisés)
* **Symptômes** : L'exécution de `docker compose up` échoue avec l'erreur `bind: address already in use` pour un port spécifique (ex: 8080, 1883, 1880, ou 5000).
* **Cause** : Un autre service sur votre machine (un ancien conteneur, un serveur IIS local, un serveur Python ou MQTT natif) occupe le port.
* **Solution** :
  1. Trouver le PID du processus responsable : `netstat -ano | findstr :1880` (remplacez 1880 par votre port).
  2. Tuer le processus depuis un terminal Administrateur : `taskkill /PID <NUMERO_PID> /F`.
  3. Ou modifier le port public dans le `docker-compose.yml` (ex: `8081:80` au lieu de `8080:80`).

---

## 2. Problèmes MQTT et EMQX

### 2.1. Le Dashboard ou l'ESP32 n'arrive pas à se connecter au Broker MQTT
* **Symptômes** : Le Dashboard reste avec le statut rouge "Connexion en cours..." ou le `mock_esp.py` boucle sur "Connection Refused".
* **Cause** : 
  - Mauvais port cible : l'ESP utilise le port MQTT natif (`1883`), tandis que le Dashboard Web a besoin du port WebSocket (`8083`).
  - Mauvaise configuration des credentials ou hôte inaccessible.
* **Solution** :
  1. Le Dashboard HTML doit pointer vers le port **8083** et l'URL path `/mqtt`.
  2. L'ESP Simulator Docker pointe vers `emqx` sur le port **1883**.
  3. Vérifiez dans `docker-compose.yml` que les variables `EMQX_ALLOW_ANONYMOUS=true` sont bien activées si l'authentification Mnesia n'est pas pleinement injectée.

### 2.2. Messages non reçus (Problèmes de QoS ou de souscription)
* **Symptômes** : L'ESP publie des données, le Dashboard est connecté au broker, mais les valeurs restent à `--` et les graphes sont statiques.
* **Cause** : Une discordance dans les topics MQTT (ex: casse différente entre `home/Sensors/dht` et `home/sensors/dht`).
* **Solution** : Le MQTT est sensible à la casse. S'assurer que le script d'envoi (`mock_esp.py`), Node-RED, et la souscription (`script.js`) portent **exactement le même nom de topic**.

---

## 3. Problèmes liés à Node-RED

### 3.1. Node-RED "Unknown Node-Type" pour ui_base (Dashboard Nodes)
* **Symptômes** : Une erreur interne Node-RED au démarrage ou lors du déploiement : unrecognised node type `ui_group` ou `ui_dashboard`.
* **Cause** : Utilisation d'un fichier `flows.json` hérité d'un projet précédent qui dépendait de `node-red-dashboard`.
* **Solution** : Le projet actuel utilise un **Dashboard Web Indépendant HTML/JS via WebSockets**. Vous pouvez supprimer les anciens noeuds "Dashboard UI" de l'interface graphique de Node-RED pour faire disparaître ces avertissements.

### 3.2. Node-RED n'arrive pas à envoyer les données au Serveur IA (Timeout ou ECONNREFUSED)
* **Symptômes** : Dans Node-RED, le noeud `HTTP Request` affiche une erreur réseau (`Error: connect ECONNREFUSED`).
* **Cause** : Le noeud HTTP pointait vers `http://localhost:5000/predict`. Depuis Node-RED conteneurisé, `localhost` désigne le conteneur Node-RED lui-même, pas la machine hôte où tournerait l'IA ni le conteneur IA lui-même.
* **Solution** : 
  - Puisque tout est dans Docker, l'URL de l'API IA dans le bloc *Node-RED* doit être : `http://ai_server:5000/predict` au lieu de `localhost`. (Le DNS de Docker-compose se charge de la résolution).

---

## 4. Problèmes du Serveur d'Intelligence Artificielle (Python)

### 4.1. L'IA crashe à cause d'un "KeyError" ou de données manquantes
* **Symptômes** : Le log Docker de l'IA affiche une Traceback `Exception on /predict [POST]` et l'API renvoie un statut 500 ou 400.
* **Cause** : Payload JSON mal formaté depuis Node-RED ou l'ESP. Ex: `{'temp': 25}` au lieu de `{'temperature': 25.0}`.
* **Solution** : Mettre en place la vérification et sécuriser le dictionnaire. Le Serveur IA doit répondre élégamment (code 400 BAD REQUEST) si les clés obligatoires `temperature` ou `humidity` sont omises.

### 4.2. Z-Score constant à 0.0 malgré de gros changements de température
* **Symptômes** : L'anomalie ne se déclenche jamais après une hausse drastique simulée.
* **Cause** : L'historique (Deque) de l'IA (requis pour calculer l'écart-type) est soit trop récent, soit écrasé.
* **Solution** : Le modèle nécessite au moins **5 valeurs successives** pour calculer sa moyenne glissante (Window History Size). Attendre 5 * 30 secondes ("Tick") pour que la détection d'anomalies s'active réellement.

---

## 5. Problèmes de Simulation Paho-MQTT (mock_esp.py)

### 5.1. AttributeError: module 'paho.mqtt.client' has no attribute 'CallbackAPIVersion'
* **Symptômes** : Le conteneur `esp_simulator` crash en boucle. Dans les logs : l'erreur mentionnée.
* **Cause** : Incompatibilité de version avec Paho-MQTT. La version v2.0 (récente) oblige à déclarer l'API version, tandis que le vieux code utilisait la v1.x.
* **Solution** : Le `docker-compose.yml` actuel installe déjà la version patchée via la commande : `pip install paho-mqtt==1.6.1` avant de lancer `mock_esp.py`. Vérifier que cette ligne n'a pas été modifiée. 

---

## 6. Problèmes sur l'Interface Web (Dashboard.html)

### 6.1. Content-Security-Policy (Mixed Content)
* **Symptômes** : L'interface web se charge mais "Paho n'est pas défini" ou impossible de se connecter.
* **Cause** : Appel à des scripts HTTP depuis une page web si celle-ci était hébergée en HTTPS. Ou accès à un WebSocket non sécurisé (`ws://`) depuis du HTTPS.
* **Solution** : Le Dashboard tourne localement sur `http://localhost:8080`, donc tout en clair. Tous les composants CDN (Chart.js et Paho MQTT) doivent être appelés via HTTPS depuis leur source (jsdelivr).

### 6.2. Les graphiques ne se remplissent pas
* **Symptômes** : Les jauges numériques s'actualisent mais les lignes graphiques (Chart.js) ne bougent pas.
* **Cause** : Manque d'espace visuel pour le canvas HTML, ou le tableau Data (les Arrays `.push`) est configuré pour écraser des données mal formées.
* **Solution** : Vérifiez l'échelle de votre Canvas dans `style.css` et assurez-vous que la fonction Javascript `addChart(v)` est bien appelée lors de la réception du message `home/sensors/dht`.

---
*Fin du document — Ce fichier doit être mis à jour à chaque fois qu'un défi technique majeur est surmonté.*
