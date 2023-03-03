import logging
import os

import discord
from dotenv import load_dotenv

from src.bot.V0 import bot


load_dotenv()

token = os.getenv('DISCORD_BOT_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot.run(token, log_handler=handler)