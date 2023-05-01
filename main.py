import logging
import os

import discord
from dotenv import load_dotenv

from src.bot.V1 import BotWrapper


load_dotenv()

token = os.getenv('DISCORD_BOT_TOKEN')
db_url = os.getenv('MONGODB_CLUSTER_URL')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
BotWrapper(db_url).run(token, log_handler=handler)