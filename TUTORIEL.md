#  Tutoriel : Explorez et Lancez le Bot Discord de DevHub

Bonjour à tous !

Ce document vous guide pour explorer, comprendre et même lancer votre propre version du bot Discord de DevHub, dont le code source est maintenant ouvert à tous. C'est une excellente opportunité d'apprendre le fonctionnement d'un bot `discord.py` avec des fonctionnalités concrètes.

## 🌟 À quoi sert ce bot ?

Ce bot a été conçu pour automatiser certaines tâches sur le serveur Discord DevHub. Ses fonctionnalités principales sont :

1.  **Publication FTP :** Il surveille certains canaux et, lorsqu'un message y est posté, il le transforme en fichier texte et l'envoie sur un site web via FTP. Parfait pour un système de news ou de partage de ressources simple.
2.  **Rappel de Bump :** Il détecte les messages du bot de "bump" (comme Disboard) et programme un rappel pour notifier le serveur lorsqu'il est à nouveau possible de "bumper".

## 🛠️ Comment l'installer et le lancer ?

Vous pouvez faire tourner une copie de ce bot sur votre propre machine pour tester et expérimenter.

### Étape 1 : Prérequis

-   Assurez-vous d'avoir [Python](https://www.python.org/downloads/) installé (version 3.8 ou plus récente).
-   Avoir un [compte Discord](https://discord.com/) et créer une application de bot sur le [Portail des Développeurs](https://discord.com/developers/applications) pour obtenir un **token**.
-   (Optionnel) Des identifiants pour un serveur FTP si vous voulez tester le module FTP.

### Étape 2 : Récupérer le code

Clonez le dépôt GitHub sur votre machine :
```bash
git clone https://github.com/gricatan/bot_discord_devhub.git
cd bot_discord_devhub
```

### Étape 3 : Installer les dépendances

Le fichier `requirements.txt` contient toutes les bibliothèques Python nécessaires. Installez-les avec `pip` :
```bash
pip install -r requirements.txt
```

### Étape 4 : Configurer le bot

Le bot utilise un fichier `.env` pour gérer les informations sensibles de manière sécurisée.

1.  Créez un nouveau fichier nommé `.env` à la racine du projet.
2.  Copiez-collez le contenu de `example.env` dans votre fichier `.env`.
3.  Modifiez les valeurs avec vos propres informations :

    ```dotenv
    # Mettez ici le token de VOTRE bot, obtenu sur le portail des développeurs Discord
    DISCORD_TOKEN=votretokensupersecret

    # Remplissez avec vos identifiants FTP (si vous testez cette fonction)
    FTP_HOSTNAME=votre.serveur.ftp
    FTP_USER=votreutilisateurftp
    FTP_PASS=votremotdepasseftp
    ```

### Étape 5 : Lancer le bot

Une fois la configuration terminée, vous pouvez démarrer le bot avec la commande suivante :
```bash
python bot_manager.py
```
Si tout va bien, la console affichera un message "Bot connecté en tant que..." et votre bot apparaîtra en ligne sur Discord !

## 🚀 Et maintenant ?

Le code est entièrement commenté pour vous aider à comprendre chaque partie. N'hésitez pas à :
-   **Lire le code :** `bot_manager.py`, `writeftp.py`, `reminder.py`.
-   **Expérimenter :** Changez des messages, modifiez la logique, ajoutez vos propres commandes.
-   **Poser des questions :** Utilisez les canaux d'entraide du serveur DevHub si vous êtes bloqué.

Bon apprentissage !
