# -*- coding: utf-8 -*-
import os
import ftplib
import asyncio
import re
import logging
import socket
from io import BytesIO
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

# --- Chargement de la configuration ---
load_dotenv()
FTP_HOSTNAME = os.getenv("FTP_HOSTNAME")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
FTP_TIMEOUT = 10  # en secondes

# Vérification des variables d'environnement FTP
if not all([FTP_HOSTNAME, FTP_USER, FTP_PASS]):
    raise ValueError("Une ou plusieurs variables d'environnement FTP sont manquantes (FTP_HOSTNAME, FTP_USER, FTP_PASS).")

# --- Logging ---
# Configuration d'un logger pour ce module spécifique pour un meilleur suivi.
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s | FTP | %(message)s")
logger = logging.getLogger("ftp_module")

# --- Mappage des Canaux ---
# Associe l'ID d'un canal Discord à un répertoire sur le serveur FTP.
# C'est ici que vous configurez quels canaux sont surveillés.
CHANNEL_FTP_MAP = {
    1426642790007439432: "/htdocs/assets/infos",
    1426643668034392176: "/htdocs/assets/challenges",
    1453369630851858523: "/htdocs/assets/projets",
}

def sanitize_filename(name: str) -> str:
    """Nettoie une chaîne pour la transformer en nom de fichier valide."""
    # Remplace tout ce qui n'est pas une lettre, un chiffre, un underscore ou un tiret par un underscore.
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def upload_to_ftp(ftp_dir: str, filename: str, content: str):
    """
    Se connecte au serveur FTP et upload un fichier texte.
    Args:
        ftp_dir (str): Le répertoire de destination sur le serveur FTP.
        filename (str): Le nom du fichier à créer.
        content (str): Le contenu à écrire dans le fichier.
    """
    logger.info(f"Tentative d'upload vers {ftp_dir}/{filename}")
    try:
        # Utilisation d'un bloc `with` pour s'assurer que la connexion est bien fermée
        with ftplib.FTP(FTP_HOSTNAME, timeout=FTP_TIMEOUT) as ftp:
            ftp.set_pasv(True)  # Mode passif, souvent nécessaire pour passer les pare-feux
            ftp.login(FTP_USER, FTP_PASS)
            logger.info("Login FTP réussi.")

            ftp.cwd(ftp_dir)
            logger.info(f"Déplacement vers le dossier : {ftp_dir}")

            # Le contenu textuel doit être encodé (en utf-8) et envoyé comme des données binaires.
            # BytesIO crée un "fichier" en mémoire.
            bio = BytesIO(content.encode("utf-8"))
            
            ftp.storbinary(f"STOR {filename}", bio)
            logger.info(f"Upload de {filename} terminé.")

            # Après chaque upload, on met à jour le fichier manifest.json
            update_manifest(ftp)

    except ftplib.all_errors as e:
        logger.error(f"Échec de l'upload pour {filename}. Erreur FTP : {e}")
    except Exception as e:
        logger.error(f"Une erreur inattendue est survenue lors de l'upload : {e}")

def update_manifest(ftp: ftplib.FTP):
    """
    Met à jour un fichier `manifest.json` à la racine du site web.
    Ce fichier contient la liste de tous les fichiers texte dans les dossiers gérés.
    """
    logger.info("Mise à jour du fichier manifest.json...")
    manifest = {}
    base_path_map = {
        1426642790007439432: "assets/infos",
        1426643668034392176: "assets/challenges",
        1453369630851858523: "assets/projets",
    }

    try:
        for channel_id, ftp_dir in CHANNEL_FTP_MAP.items():
            key = base_path_map.get(channel_id, str(channel_id))
            try:
                ftp.cwd(ftp_dir)
                # Liste les fichiers se terminant par .txt
                txt_files = [f for f in ftp.nlst() if f.endswith(".txt")]
                manifest[key] = [f"{base_path_map[channel_id]}/{f}" for f in txt_files]
            except ftplib.all_errors as e:
                logger.warning(f"Impossible de lister le répertoire {ftp_dir}: {e}")
                manifest[key] = []

        # Prépare le contenu JSON
        content = json.dumps(manifest, indent=2)
        bio_manifest = BytesIO(content.encode("utf-8"))
        
        # Se déplace à la racine et uploade le manifest
        ftp.cwd("/htdocs")
        ftp.storbinary("STOR manifest.json", bio_manifest)
        logger.info("Fichier manifest.json mis à jour avec succès.")
        
    except ftplib.all_errors as e:
        logger.error(f"Échec de la mise à jour du manifest.json : {e}")
    except Exception as e:
        logger.error(f"Erreur inattendue lors de la mise à jour du manifest : {e}")


def start_ftp_modules(bot: commands.Bot):
    """Initialise les événements de ce module et les attache au bot."""

    @bot.event
    async def on_message(message: discord.Message):
        # Ignore les messages des bots pour éviter les boucles
        if message.author.bot:
            return

        # Ne traite que les messages des canaux configurés
        if message.channel.id not in CHANNEL_FTP_MAP:
            return

        ftp_dir = CHANNEL_FTP_MAP[message.channel.id]
        logger.info(f"Message reçu dans un canal mappé : #{message.channel.name}")

        # La logique de formatage dépend du canal
        if message.channel.id in (1426642790007439432, 1426643668034392176):
            lines = message.content.splitlines()
            if not lines:
                logger.warning("Message vide, upload ignoré.")
                return

            # La première ligne est le nom du fichier, le reste est le contenu
            filename = sanitize_filename(lines[0].strip()) + ".txt"
            content = "\n".join(lines[1:]).strip()

            if not content:
                logger.warning("Contenu vide après le titre, upload ignoré.")
                return

            # Exécute la fonction d'upload (qui est bloquante) dans un thread séparé
            # pour ne pas bloquer le bot.
            await bot.loop.run_in_executor(None, upload_to_ftp, ftp_dir, filename, content)

    @bot.event
    async def on_thread_create(thread: discord.Thread):
        # Ne s'applique qu'aux threads créés dans le canal "projets"
        if thread.parent_id != 1453369630851858523:
            return

        logger.info(f"Nouveau thread de projet détecté : '{thread.name}'")

        try:
            # Récupère le tout premier message du thread pour en extraire le contenu
            start_message = await thread.fetch_message(thread.id)
            
            if start_message and not start_message.author.bot:
                filename = sanitize_filename(thread.name) + ".txt"
                content = start_message.content.strip()
                ftp_dir = CHANNEL_FTP_MAP[thread.parent_id]

                if not content:
                    logger.warning("Message initial du thread vide, upload ignoré.")
                    return
                
                await bot.loop.run_in_executor(None, upload_to_ftp, ftp_dir, filename, content)
            
        except discord.NotFound:
            logger.error(f"Impossible de trouver le message initial du thread {thread.id}")
        except Exception as e:
            logger.error(f"Erreur lors du traitement du thread {thread.name}: {e}")

    logger.info("Module FTP chargé et événements prêts.")
