# -*- coding: utf-8 -*-
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# --- Modules locaux ---
from writeftp import start_ftp_modules
from reminder import start_reminder

# --- Chargement de la configuration ---
# Charge les variables d'environnement à partir du fichier .env
load_dotenv() 
TOKEN = os.getenv("DISCORD_TOKEN")

# Vérification de la présence du token
if TOKEN is None:
    raise ValueError("Le DISCORD_TOKEN n'a pas été trouvé dans le fichier .env")

# --- Configuration du bot ---
# Définition des "intents" (intentions) du bot.
# Celles-ci déterminent les types d'événements que le bot recevra de Discord.
intents = discord.Intents.default()
intents.members = True  # Reçoit les événements liés aux membres (arrivée, départ)
intents.messages = True  # Reçoit les événements liés aux messages (nouveau message, suppression)
intents.message_content = True  # Nécessaire pour lire le contenu des messages, requiert une activation dans le portail développeur Discord.

# Création de l'instance du bot avec un préfixe de commande et les intents
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Initialisation des modules externes ---
# Chaque module peut contenir ses propres commandes et événements.
# On passe l'instance du bot à chaque fonction d'initialisation.
start_ftp_modules(bot)
start_reminder(bot)

# --- Événement "on_ready" ---
# Cet événement est appelé lorsque le bot a terminé sa connexion à Discord.
@bot.event
async def on_ready():
    """Affiche un message dans la console lorsque le bot est prêt."""
    print(f"Bot connecté en tant que : {bot.user}")
    print("------")

# --- Commande de test ---
@bot.command(name="ping", help="Vérifie la latence du bot.")
async def ping(ctx):
    """Commande simple pour s'assurer que le bot répond."""
    await ctx.send(f"Pong ! ({round(bot.latency * 1000)}ms)")

# --- Lancement du bot ---
# Exécute le bot avec le token récupéré.
bot.run(TOKEN)
