# 🧠 Prompt Structuré pour Générateur de Slides (Gamma / Canva / IA)

Ce document est spécialement formaté pour être ingéré par une Intelligence Artificielle génératrice de présentation. Chaque diapositive est structurée avec un titre clair, du texte très concis, et un **grand espace explicite** réservé pour l'insertion de vos captures d'écran, incluant un focus profond sur l'interface Docker Desktop.

---

### Slide 1 : Page de Garde
**Titre :** SmartHome AI Monitor — Système IoT Prédictif
**Texte :**
* De l'IoT au Machine Learning Conteneurisé.
* Projet de Module IoT - ENSA FÈS.
* Nom, Encadrant (Pr. Balboul Younes), Année Universitaire.
**[ 🖼️ ESPACE IMAGE : Insérer le Logo de l'ENSA Fès au centre, et une miniature du Dashboard en arrière-plan ]**

### Slide 2 : Le Plan de la Soutenance
**Titre :** Sommaire
**Texte :**
* 1. Contexte & Problématique Industrielle
* 2. Stack Technique Détaillée (A-Z)
* 3. Architecture et Problématiques Matérielles
* 4. Orchestration Node-RED & Intelligence Artificielle
* 5. Infrastructures Docker (Desktop, Composants, Pannes)
* 6. Interface Graphique et Dashboard
* 7. Tests de Robustesse & Conclusion
**[ 🖼️ ESPACE IMAGE : Icônes représentant chaque étape (Hardware, Docker, Cerveau IA, Écran) ]**

### Slide 3 : Contexte de l'Internet des Objets (IoT)
**Titre :** Le Basculement vers l'Age Prédictif
**Texte :**
* L'IoT classique est "Réactif" : il attend la panne pour biper.
* L'IoT moderne (AIoT) est "Prédictif" : il anticipe les pannes matérielles.
* Les enjeux : Maintien des Datacenters et des chaines de froid.
**[ 🖼️ ESPACE IMAGE : Graphique abstrait ou photo d'une salle de serveurs (Data Center) ]**

### Slide 4 : La Problématique Industrielle Centrale
**Titre :** L'inertie thermique tue le matériel
**Texte :**
* Les systèmes locaux basculent un relais sur la base d'un simple seuil (ex: si T > 30°C).
* **Le Problème :** À cause de l'inertie thermique, lorsqu'une salle dépasse un seuil fixe, le matériel est souvent déjà endommagé.
**[ 🖼️ ESPACE IMAGE : Capture d'écran du Dashboard actuel montrant la courbe thermique approchant la ligne rouge critique ]**

### Slide 5 : Notre Solution et Objectifs Technologiques
**Titre :** Architecture End-to-End
**Texte :**
* **Captation :** Télémétrie haute fréquence via microcontrôleurs Wi-Fi.
* **Traitement :** Analyse probabiliste (Z-Score) via un serveur Python local en temps réel.
* **Action :** Renvoi de l'ordre d'urgence (Ventilation/Alarme) via MQTT.
**[ 🖼️ ESPACE IMAGE : Grand schéma global vectoriel de l'architecture : ESP32 ➔ EMQX ➔ Node-RED ➔ Serveur IA ]**

### Slide 6 : Stack IoT & Hardware (ESP32)
**Titre :** Le Matériel : Microcontrôleur et Capteur
**Texte :**
* **Puce :** ESP32 (Xtensa Dual-Core) avec Wi-Fi natif.
* **Capteur :** DHT22 (Lecture numérique précise de la Température/Humidité).
* **Firmware :** MicroPython 1.20+ (Modules `machine`, `network`, `umqtt.simple`).
**[ 🖼️ ESPACE IMAGE : Photo d'une carte ESP32 physical ou schéma Wokwi du circuit complet avec les deux relais (Climatiseur/Alarme) ]**

### Slide 7 : Stack Messagerie & Routage (EMQX)
**Titre :** Le Coeur du Réseau : MQTT
**Texte :**
* **Protocole :** MQTT. Poids ultra-léger, adapté aux réseaux instables.
* **Broker EMQX :** v5.8.0. Technologie Erlang industrielle.
* **Double interface :** TCP pur (port 1883) pour les puces physiques, et WebSocket (port 8083) pour le navigateur web.
**[ 🖼️ ESPACE IMAGE : Capture d'écran du Dashboard d'Administration EMQX (localhost:18083) montrant les "Connections" ]**

### Slide 8 : Stack Orchestration & Logique (Node-RED)
**Titre :** L'Aiguilleur des Données
**Texte :**
* **Outil :** Node-RED (Node.js). Programmation visuelle asynchrone bas-niveau.
* **Utilité :** Traduire le binaire MQTT vers du HTTP (POST) pour le serveur Python, sans alourdir le code IA.
**[ 🖼️ ESPACE IMAGE : Capture d'écran large et bien lisible du Flux (Flow) de base dans l'interface Node-RED ]**

### Slide 9 : Stack Intelligence Artificielle (Python)
**Titre :** Le Cerveau du Système
**Texte :**
* **Langage & WebServer :** Python 3.9 avec `Flask` pour écouter les données POST en continu.
* **Détection d'Anomalie :** `scipy.stats` (Algorithme Z-Score statique sur fenêtre glissante).
* **Prédiction :** `scikit-learn` (Régression linéaire pour estimer H+5 mins).
**[ 🖼️ ESPACE IMAGE : Capture d'écran d'un extrait du code Python (ex: la fameuse fonction mathématique de détection Z-score) ]**

### Slide 10 : Stack Frontend UI/UX
**Titre :** L'Interface Client
**Texte :**
* **Architecture :** Single Page App. Zéro framework lourd (Pas de React/Angular).
* **Rendu temps réel :** HTML5, CSS3 vectoriel luxueux, et `Chart.js` pour des graphiques Canvas à 60 FPS.
* **Liaison temps réel :** Librairie `Paho-MQTT 1.0.1` client WebSocket.
**[ 🖼️ ESPACE IMAGE : Capture d'écran de l'UI finale (Interface Bleu Nuit/Or), focalisée sur la bannière de haut d'écran ]**

### Slide 11 : Le Défi de la Simulation (Wokwi vs Physique)
**Titre :** Problème Matériel N°1
**Texte :**
* Le développement avec une puce physique branchée 24h/24 par USB cause des déconnexions aléatoires impossibles à débugger.
* Choix de se tourner vers la virtualisation logicielle (Wokwi au sein de VS Code).
**[ 🖼️ ESPACE IMAGE : Capture de l'ancien bug Wokwi ou du panel de droite Wokwi VS Code avec les composants branchés virtuellement ]**

### Slide 12 : La Panne Critique Wokwi (DTR/RTS)
**Titre :** La Boucle de Reset Asynchrone
**Texte :**
* **Le Bug :** Le transfert du code Python vers l'émulateur plantait en "Watchdog Reset" infini à cause des signaux de contrôle terminaux (DTR/RTS) bloquants.
* **La Solution Ingénieur :** Contournement total via l'invention du script `inject_code.py` communiquant en pur **Raw TCP Sockets** avec la mémoire Wokwi.
**[ 🖼️ ESPACE IMAGE : Capture d'écran du code `inject_code.py` ou du terminal montrant l'injection réussie ("BYTES INJECTED") ]**

### Slide 13 : Transition vers un Simulateur Dockerisé
**Titre :** Maturité du Projet
**Texte :**
* **Limite Wokwi :** La génération "aléatoire" pure fausse l'Intelligence Artificielle.
* **Solution Ultime :** Création d'un module de simulation 100% natif en Python `mock_esp.py`.
* **Réalisme :** Génération de vraies courbes sinusoïdales (climat journalier) via `math.sin` !
**[ 🖼️ ESPACE IMAGE : Capture d'écran de la console du simulateur Docker (`docker logs esp_simulator`) affichant l'avancement "Normal -> Anomalie" ]**

### Slide 14 : Infrastructure : Pourquoi Docker ?
**Titre :** L'approche Containerisation
**Texte :**
* **Problème :** Le syndrome "Ça marche sur ma machine".
* **Solution :** Docker encapsule toutes les bibliothèques et chaque microservice (Node, Python, EMQX) dans une boite inviolable et mobile.
**[ 🖼️ ESPACE IMAGE : Capture du Fichier `docker-compose.yml` (zoom sur la liste des différents "services:") ]**

### Slide 15 : Vue Interne Docker Desktop (Images)
**Titre :** L'Espace Images Locales
**Texte :**
* Sur **Docker Desktop**, nous gérons nos couches images de base (ex: `python:3.9-slim`, `emqx/emqx:5.8.0`).
* Poids très optimisé (Images *alpine* et *slim*) consommant peu d'espace disque.
**[ 🖼️ ESPACE IMAGE : Capture d'écran de Docker Desktop orientée sur le volet gauche "Images", affichant la liste des images téléchargées avec leur taille en MB ]**

### Slide 16 : Vue Interne Docker Desktop (Containers)
**Titre :** Orchestration et Conteneurs Actifs
**Texte :**
* Le Hub central permet de visualiser l'état de nos 5 services "Running" en temps réel.
* Permet également d'accéder aux statistiques CPU/RAM et aux logs internes instantanément.
**[ 🖼️ ESPACE IMAGE : Capture d'écran de Docker Desktop focalisée sur l'onglet "Containers", avec les indicateurs verts montrant que tout tourne ]**

### Slide 17 : Analyse des Logs Docker
**Titre :** Monitoring Terminal Docker
**Texte :**
* Suivi des événements d'Intelligence Artificielle et pannes directement depuis le système hôte.
* Isolation des erreurs réseaux et matérielles propre à chaque microservice.
**[ 🖼️ ESPACE IMAGE : Capture d'écran du terminal Docker Desktop en train d'afficher les logs du `ai_server` ou du `nodered` ]**

### Slide 18 : Le Problème Réseau Docker (Bridge Isolation)
**Titre :** Problème Infrastructuriel N° 1
**Texte :**
* **Le Bug :** Impossible pour le Dashboard Web de récupérer les données, erreur CORS/Network.
* **Raison :** Le conteneur Docker forme un réseau caché invisible pour Windows/Navigateur.
* **Solution :** Utilisation intensive du `Ports Mapping` (`1883:1883`) et non des IP internes.
**[ 🖼️ ESPACE IMAGE : Capture d'écran de l'onglet Réseaux (Network) de Docker ou zoom sur la directive "ports:" dans docker-compose ]**

### Slide 19 : Le Cauchemar EBUSY sous Windows
**Titre :** Problème Infrastructuriel N° 2 (EBUSY Node-RED)
**Texte :**
* **Le Bug Fatal :** Lors du développement Node-RED, sauvegarder déclenchait `Resource busy or locked`. Crash total.
* **Cause :** L'environnement WSL2 Windows verrouille l'accès direct aux fichiers Linux (File Lock Atomique).
**[ 🖼️ ESPACE IMAGE : Capture d'écran du terminal rouge affichant l'erreur EBUSY Node-RED ! ]**

### Slide 20 : La Solution EBUSY : Les Volumes Linux
**Titre :** Persistance des Données (Docker Volumes)
**Texte :**
* Remplacement du dossier de montage (`bind-mount`) lié à Windows par un **Named Volume Docker**.
* Node-RED détient maintenant un espace disque purement Linux (EXT4) géré par le daemon. Adieu les crashes !
**[ 🖼️ ESPACE IMAGE : Capture d'écran sur l'onglet "Volumes" intérieur de Docker Desktop. Ou le code du volume `nodered_data` en Yaml ]**

### Slide 21 : Topologie et Flow Node-RED Final
**Titre :** Traduction MQTT -> HTTP
**Texte :**
* Le flux écoute le topic `home/wokwi/sensors/dht`.
* Nettoie les données (NaN exception) via une fonction Javascript interne.
* Poste le tout au port `5000` de l'IA (Flask).
**[ 🖼️ ESPACE IMAGE : Très grosse capture d'écran du noeud `function` de nettoyage Javascript présent à l'intérieur de Node-RED ]**

### Slide 22 : Le Retour d'Information (Feedback Loop)
**Titre :** Gérer les Ordres Actionneurs
**Texte :**
* Lorsque l'IA détecte une anomalie, l'ordre est renvoyé à Node-RED, qui effectue un "MQTT Out".
* Utilisation de la **QoS 1** ("At least once") pour certifier que l'ordre du ventilateur/Vanne est bien reçu.
**[ 🖼️ ESPACE IMAGE : Capture d'écran du Noeud MQTT-Out de Node-Red montrant le paramètre "QoS 1" ciblé sur `home/wokwi/#` ]**

### Slide 23 : Le Cœur Mathématique (Algorithme 1 - ZScore)
**Titre :** Détection d'Anomalie Soudaine
**Texte :**
* Le Z-Score mesure l'écart d'une valeur par rapport à la moyenne historique des 20 dernières mesures tamponnées en FIFO RAM.
* Ignorer la météo ambiante pour ne voir que **l'accélération brutale** invisible à l'œil nu.
**[ 🖼️ ESPACE IMAGE : Extrait hyper clair du code `z = abs((temp - mean_temp) / std_temp)` ou la liste buffer Python ]**

### Slide 24 : Le Cœur Mathématique (Algorithme 2 - Régression OLS)
**Titre :** Régression Linéaire et Prédiction
**Texte :**
* Entraînement dynamique immédiat de `Scikit-Learn` basé sur les "timestamps" locaux (Axe des x).
* Extrapolation du point $Y$ à "$Temps \ actuel + 5 \ minutes$".
**[ 🖼️ ESPACE IMAGE : Extrait du code `model.fit(X, y)` et `model.predict(5 mins)` de votre serveur IA Python ]**

### Slide 25 : Refonte UI et Design Exclusif
**Titre :** L'Interface SmartHome Premium
**Texte :**
* Abandon pur et simple des interfaces étudiantes basiques (emojis/couleurs discordantes).
* Mise en place d'un design système professionnel : "Marine Blue & Gold", iconographie SVG stricte vectorielle.
**[ 🖼️ ESPACE IMAGE : Avant/Après (Petit screenshot du vieux tableau blanc de base, vs Grand screenshot du dashboard actuel dark-modé) ]**

### Slide 26 : Rendu Graphique Hautes Performances
**Titre :** Data Visualization
**Texte :**
* Les données MQTT génèrent des points sur `Chart.js` instantanément.
* Superposition de la thermométrie et de l'Hygrométrie, plus ligne seuil à 30°C pour référence physique visuelle.
**[ 🖼️ ESPACE IMAGE : Zoom très ciblé pris sur l'écran du Dashboard, montrant UNIQUEMENT la boîte contenant la charte Chart.Js multicolore ]**

### Slide 27 : Le Sparkline Prédictif
**Titre :** Affichage de la tendance l'Avenir
**Texte :**
* Affichage direct du résultat de la régression linéaire sur le dashboard (Card "Prédiction +5 min").
* Indication visuelle texte (Hausse prévue, baisse prévue).
**[ 🖼️ ESPACE IMAGE : Capture d'écran cadrée spécifiquement sur le petit rectangle "Détection IA" et "Prédiction + 5 min" du Dashboard web ]**

### Slide 28 : Systèmes d'Alertes Tolérants (HMI)
**Titre :** Avertir l'Opérateur en direct
**Texte :**
* Disparition du passif. Si Z-Score > 2.5, injection dynamique CSS.
* Apparition d'une bannière rouge vif (Header Alarm) incitant au réflexe de contrôle.
* Toast Notifications (Bottom Right) logguant chaque commande MQTT et les réussites QoS 1.
**[ 🖼️ ESPACE IMAGE : Capture d'écran du Dashboard au moment exact où la grosse BANNIERE ROUGE est active en haut ! Et capture d'un petit Toast Vert ]**

### Slide 29 : Démonstration et Contrôle Relais
**Titre :** Actionneurs Symétriques
**Texte :**
* Le tableau de commande Dashboard offre des interrupteurs asynchrones, basés non pas sur le clic... mais sur le "Status Confirmed" renvoyé par l'ESP32. (Led UI rouge devient Verte `uniquement` par confirmation EMQX).
**[ 🖼️ ESPACE IMAGE : Capture d'écran du bloc "Relais 1 - Climatiseur" sur le dashboard web ]**

### Slide 30 : Les Événements en Ligne de Commande UI
**Titre :** Event Log Client
**Texte :**
* Implémentation d'un mini-terminal de log intégré à l'UI pour auditer chaque message MQTT public EMQX.
**[ 🖼️ ESPACE IMAGE : Capture du bloc "Journal des Événements MQTT" en bas à gauche de votre dashboard ]**

### Slide 31 : Validation : Tests avec MQTTX
**Titre :** Outils de Tests Architecturaux Externes
**Texte :**
* Pour prouver le fonctionnement multi-clients Open Architecture, nous avons manipulé et piraté nos flux capteurs avec l'application "MQTTX".
* Vérification pure via connexion "TLS SSL" et "Port 8084" cryptés ignorés par Node-RED.
**[ 🖼️ ESPACE IMAGE : Logiciel MQTTX Client ou son interface Web affichant les lignes de JSON entrants en console (Sniffing) ]**

### Slide 32 : Monitoring et Performances du Brokage
**Titre :** Benchmarking Système M2M
**Texte :**
* Le projet est hébergé sans latence, avec plus de 3 clients simultanés connectés par Seconde.
* Charge processeur imperceptible grâce au moteur C de Python (Flask) et à Erlang (MQTT). Efficacité prouvée.
**[ 🖼️ ESPACE IMAGE : Capture de la page d'accueil d'admin EMQX `localhost:18083` montrant la charge CPU Node Linux ou le nombre total de messages transférés ]**

### Slide 33 : Synthèse Pédagogique (1/2)
**Titre :** Bilan Multidisciplinaire
**Texte :**
* **Électronique :** Signaux DTR/RTS, bus numériques, GPIO Hardware ESP.
* **Réseaux & Infrastructures :** MQTT, Qualité de Service (QoS), TCP/IP vs WebSockets.
**[ 🖼️ ESPACE IMAGE : Collages de petits logos : Node, Python, ESP32, MQTT ]**

### Slide 34 : Synthèse Pédagogique (2/2)
**Titre :** Bilan Multidisciplinaire Avancé
**Texte :**
* **Mathématiques & IA :** Z-Score Statistique Temps Réel, Régression Machine Learning OLS scikit-learn.
* **DevOps :** Maîtrise des environnements conteneurisés Docker, problèmes Root OS Linux/Windows, Named Volumes, Isolated Bridge Networks.
**[ 🖼️ ESPACE IMAGE : Collages de petits logos : Docker, Scipy, Wokwi ]**

### Slide 35 : Conclusion & Q&A
**Titre :** Évolutions Futures
**Texte :**
* Basculement vers des Réseaux Protégés MQTTS (Certificats Let's Encrypt).
* Intégration d'InfluxDB pour sauvegarder des millions de points sur SSD via Volume Docker Persistant.
* **Merci de votre attention ! Avez-vous des Questions ?**
**[ 🖼️ ESPACE IMAGE : Très très belle capture totale en Plein Écran de votre magnifique Dashboard avec le graphique rouge et or s'envolant. Le meilleur screen doit être à la fin. ]**
