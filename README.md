# Bot Discord Multifonctions pour DevHub

Ce projet est un bot Discord conçu pour le serveur DevHub. Il intègre plusieurs modules pour automatiser des tâches telles que la publication de contenu via FTP et l'envoi de rappels pour "bumper" le serveur.

## Fonctionnalités

-   **Gestionnaire de Bot Principal (`bot_manager.py`)**:
    -   Point d'entrée du bot.
    -   Charge tous les modules externes.
    -   Utilise des variables d'environnement pour une configuration sécurisée.
    -   Contient une commande de base `!ping` pour vérifier la réactivité du bot.

-   **Module FTP (`writeftp.py`)**:
    -   Surveille des canaux Discord spécifiques.
    -   Lorsqu'un message est posté dans un canal surveillé, son contenu est transformé en fichier `.txt` et uploadé sur un serveur FTP.
    -   Le nom du fichier est tiré de la première ligne du message, le contenu du reste.
    -   Gère également la création de fichiers à partir de threads dans les forums.
    -   Met à jour un fichier `manifest.json` sur le serveur web pour lister dynamiquement les contenus.

-   **Module de Rappel (`reminder.py`)**:
    -   Surveille les messages d'un bot spécifique (par exemple, Disboard) dans un canal dédié.
    -   Lorsqu'un message de "bump" est détecté, il programme un rappel qui sera envoyé après un délai configurable (par défaut 2 heures).

## Prérequis

-   Python 3.8 ou supérieur
-   Un compte Discord et un bot créé sur le [Portail des Développeurs Discord](https://discord.com/developers/applications).
-   Les identifiants d'un serveur FTP.

## Installation

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/VOTRE_NOM/VOTRE_REPO.git
    cd VOTRE_REPO
    ```

2.  **Installez les dépendances :**
    Il est recommandé d'utiliser un environnement virtuel, mais pas obligatoire pour un simple test.
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Le bot se configure à l'aide d'un fichier `.env`.

1.  **Créez un fichier `.env`** à la racine du projet.
2.  **Copiez le contenu** du fichier `example.env` et collez-le dans votre nouveau fichier `.env`.
3.  **Remplissez les valeurs** avec vos propres informations :

    ```dotenv
    # Token de votre bot Discord
    DISCORD_TOKEN=votretokensupersecret

    # Informations de connexion FTP
    FTP_HOSTNAME=votre.serveur.ftp
    FTP_USER=votreutilisateurftp
    FTP_PASS=votremotdepasseftp
    ```

    **Important** : Assurez-vous que le fichier `.env` n'est jamais partagé ou publié sur GitHub. Le fichier `.gitignore` inclus dans ce projet l'exclut déjà.

## Démarrage du Bot

Pour lancer le bot, exécutez le script `bot_manager.py` :

```bash
python bot_manager.py
```

Si tout est configuré correctement, vous devriez voir un message dans votre console indiquant que le bot est connecté.

---
*Projet préparé avec l'aide de l'assistant Gemini.*
