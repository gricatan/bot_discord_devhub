# -*- coding: utf-8 -*-
import asyncio
import discord
from discord.ext import commands

# --- Configuration du Rappel ---
# ID du bot dont il faut surveiller les messages (ex: Disboard)
BUMP_BOT_ID = 302050872383242240
# ID du canal où les messages de "bump" sont postés
BUMP_CHANNEL_ID = 1430291116359417907
# Texte du message de rappel
REMINDER_TEXT = "⏰ C'est l'heure de remonter le serveur ! Utilisez la commande `/bump`."
# Délai en heures avant d'envoyer le rappel
DELAY_HOURS = 2

def start_reminder(bot: commands.Bot):
    """
    Initialise les événements pour le module de rappel de "bump".
    """

    @bot.event
    async def on_message(message: discord.Message):
        """
        Déclenché à chaque message. Vérifie si c'est un message de bump
        pour programmer un rappel.
        """
        # On ne s'intéresse qu'aux messages du bot de bump dans le canal spécifié.
        if message.author.id != BUMP_BOT_ID or message.channel.id != BUMP_CHANNEL_ID:
            return

        # On vérifie si le message du bot est bien une confirmation de bump réussi.
        # Adaptez cette condition au message réel envoyé par votre bot de bump.
        # Ici, on suppose qu'un embed avec "Bump effectué !" est envoyé.
        if message.embeds and "Bump effectué !" in message.embeds[0].description:
            print(f"Bump détecté. Programmation du rappel dans {DELAY_HOURS} heure(s).")
            
            # Lance la tâche de rappel en arrière-plan.
            asyncio.create_task(send_reminder(message.channel))

    async def send_reminder(channel: discord.TextChannel):
        """
        Attend un délai défini puis envoie un message de rappel.
        """
        # Conversion des heures en secondes
        await asyncio.sleep(DELAY_HOURS * 3600)
        
        print(f"Envoi du rappel de bump dans le canal #{channel.name}.")
        await channel.send(REMINDER_TEXT)

    print("Module de rappel de bump chargé.")