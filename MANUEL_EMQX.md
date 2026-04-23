# 📘 Manuel d'Utilisation : EMQX Edge MQTT Broker

Ce manuel décrit précisément comment utiliser l'interface d'administration de **EMQX** (le broker MQTT) fourni dans notre infrastructure Docker (Edge Computing) pour la soutenance du projet SmartHome Monitor.

---

## 1. À quoi sert le Broker EMQX Local (L'approche Edge) ?

Dans le cadre du projet, vous utilisez par défaut le broker public gratuit `broker.emqx.io` (via Internet) pour des raisons de simplicité de test.
**Cependant**, l'architecture Docker lance en arrière-plan **votre propre instance privée de EMQX**. C'est ce qu'on appelle la philosophie **"Edge Computing"** (informatique à la périphérie) :
- Les données restent strictement à l'intérieur du réseau local du domicile.
- Aucune dépendance à une connexion Internet externe.
- Latence quasi-nulle.
- Sécurité renforcée grâce aux identifiants locaux.

C'est un atout technique MAJEUR à présenter lors de votre soutenance.

---

## 2. Accéder à l'Interface d'Administration

EMQX dispose d'un panneau de contrôle visuel très puissant, l'**EMQX Dashboard**.

1. Démarrez votre environnement Docker (`.\start.bat`).
2. Ouvrez un navigateur et allez sur : **[http://localhost:18083](http://localhost:18083)**
3. L'écran de connexion s'affiche.
4. Utilisez les identifiants configurés de base dans notre projet :
   - **Utilisateur :** `admin`
   - **Mot de passe :** `adminensaf1`

---

## 3. Que montrer au Professeur pendant la démo ?

Une fois connecté à l'interface EMQX, voici les écrans intéressants à présenter pour justifier l'architecture robuste du projet :

### A. Onglet "Overview" (Vue d'ensemble)
- Montre le trafic en direct : le nombre de connexions actuelles, les messages envoyés/reçus par seconde (les "publish" et "subscribe").
- Prouve que le courtier MQTT est capable d'encaisser un fort volume de télémétrie de manière asynchrone (QoS 0, 1, 2).

### B. Onglet "Clients"
- Liste de manière transparente tous les équipements connectés à l'instant T (votre Dashboard Web, Node-RED, et éventuellement l'ESP32).
- Expliquez que vous voyez directement si un capteur tombe "Offline", ce qui facilite le débogage (les messages de type *Will Message* peuvent y être analysés).

### C. L'outil "WebSocket Client" intégré (Outil de Test)
- EMQX Dashboard inclut un client de test directement dans le navigateur !
- Allez dans la section `Tools` -> `WebSocket`.
- Cliquez sur **Connect**. Dans `Subscription`, entrez `home/wokwi/sensors/dht` et cliquez sur "Subscribe".
- Vous verrez passer le trafic brut JSON du capteur en direct. Cela montre que vous comprenez parfaitement la mécanique bas niveau du Publish/Subscribe.

---

## 4. Passer du mode "Public" au mode "100% Local" (Optionnel mais impressionnant)

Imaginons que vous vouliez faire une démonstration à votre professeur en lui disant : *"Regardez, même si je coupe l'accès internet (wifi du téléphone coupé), notre maison connectée fonctionne"* :

1. Ouvrez le fichier **`wokwi_main.py`** et modifiez l'adresse :
   ```python
   MQTT_BROKER = '127.0.0.1'  # Au lieu de 'broker.emqx.io'
   ```
2. Ouvrez votre **`dashboard.html`** et à la ligne 170, modifiez :
   ```javascript
   const BROKER    = "127.0.0.1";  /* Au lieu de broker.emqx.io */
   ```
3. Relancez la page et le simulateur Wokwi. 
**Résultat :** Tout votre trafic transite désormais anonymement et ultra-rapidement sur la boucle locale locale grâce au container Docker EMQX. C'est l'essence même de l'informatique industrielle !
