# Mode d'Emploi Rapide (Quickstart) - Ligne de Commande & Wokwi (VS Code)

Ce projet orchestre un réseau IoT complet avec un back-end conteneurisé (Docker) et un front-end ESP32 émulé avec **l'extension Wokwi sous Visual Studio Code**. 

---

## 🛠️ Étape 0 : Préparation (Sur une nouvelle Machine)
1. Installez `Docker Desktop` (avec l'option WSL 2 activée sous Windows).
2. Vérifiez dans votre terminal que Docker répond :
```cmd
docker --version
```
3. Ouvrez le dossier du projet **SmartHomeMonitor** dans Visual Studio Code.
4. Assurez-vous d'avoir installé l'extension **Wokwi Simulator** dans VS Code.


## 🚀 Étape 1 : Démarrage du Back-end (Serveur IA, EMQX, Node-RED, Dashboard)
Ouvrez le terminal intégré de VS Code (`Terminal -> Nouveau Terminal`) et activez les conteneurs :

```cmd
.\start.bat
```
*(Laissez le terminal ouvert pendant son exécution. Le premier téléchargement peut nécessiter l'autorisation du Pare-feu Windows).*


## 🏎️ Étape 2 : Démarrage de l'ESP32 dans Wokwi (Méthode inject.bat)
C'est ici qu'intervient la simulation matérielle. L'ESP32 s'exécute nativement via le client Wokwi officiel et s'interface avec le réseau via le port 4000 :

1. Dans votre explorateur de fichiers, double-cliquez sur :
   **👉 `start_wokwi.bat`**
2. Le simulateur démarrera dans votre navigateur et le port 4000 s'ouvrira en coulisse. Attendez que la page Wokwi soit chargée.
3. Pour envoyer votre programme instantanément, double-cliquez sur :
   **👉 `inject.bat`**
4. **Magie :** Wokwi téléverse le fichier `main.py` et s'anime immédiatement. L'ESP32 se connectera à EMQX et enverra ses capteurs !


## 📊 Étape 3 : Accès aux adresses web
Ouvrez votre navigateur internet et tapez ces URL exactes :

* **Dashboard Web Central** : http://localhost:8080 (Les données produites par Wokwi vont s'afficher ici)
* **Serveur IA** : http://localhost:5000/status
* **Orchestrateur Node-RED** : http://localhost:1880
* **Admin Broker EMQX** : http://localhost:18083 *(Login: `admin` / Password: `adminensaf1`)*


## 🛑 Étape 4 : Arrêt Propre 
À la fin de l'évaluation ou de votre cours, arrêtez Wokwi (Bouton Stop carré rouge) et n'oubliez pas de nettoyer les conteneurs Docker pour éviter de saturer la machine :
```cmd
docker compose down
```
