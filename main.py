import os
import time
from dotenv import load_dotenv

import discord
from discord.ext import tasks, commands

from myges import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
global time
time = 0

@bot.event
async def on_ready():
  task_loop.start()
  print("Conection Ok!")

@tasks.loop(hours=168)
async def task_loop():
  print('Check planning')
  channel = bot.get_channel(1053333090908520541)
  message = start()
  await channel.send(message)
  print('End !')

@bot.command(name='planning')
async def getPlanning(ctx):
  message = start()
  await ctx.send(message)
  print('End !')

@bot.command(name='clear')
async def clear(ctx, amount=10):
  await ctx.channel.purge(amount)



bot.run(os.getenv("TOKEN"))
