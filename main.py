import os
from dotenv import load_dotenv

import discord
from discord.ext import tasks, commands

import request as Request
import verification as Verification
import myges as MyGes

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
request = Request.start()

async def sessionValidity(channel) :
  status = Verification.getSessionValidity(request)

  while status == -1 :
    await channel.send("❌ Erreur de session")
    await channel.send("⏳ Regénération de la session")
    status = Verification.getSessionValidity(request)

  await channel.send("✅ Session valide")

@bot.event
async def on_ready():
  task_loop.start()
  print("Conection Ok!")

@tasks.loop(hours=168)
async def task_loop():
  channel = bot.get_channel(1053333090908520541)
  sessionValidity(channel)
  print('Check planning')
  message = MyGes.start()
  print(message)
  # await channel.send(message)
  print('End !')

@bot.command(name='planning')
async def getPlanning(ctx):
  message = MyGes.start()
  await ctx.send(message)
  print('End !')

@bot.command(name='clear')
async def clear(ctx, amount=10):
  await ctx.channel.purge(amount)



bot.run(os.getenv("TOKEN"))
