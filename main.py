import os
import time
from dotenv import load_dotenv

import discord
from discord.ext import tasks, commands

from myges import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
separator = "###########"

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
  result = start()
  await channel.send(separator)
  for element in result :
    await channel.send(element)
  await channel.send(separator)
  print('End !')

@bot.command(name='planning')
async def lunch_royaltiz(ctx):
  result = start()
  await ctx.send(separator)
  for element in result :
    await ctx.send(element)
  await ctx.send(separator)
  print('End !')

@bot.command(name='clear')
async def clear(ctx, amount=10):
  await ctx.channel.purge(amount)



bot.run(os.getenv("TOKEN"))
