import os
from dotenv import load_dotenv

import discord
from discord.ext import tasks, commands

import request as Request
import verification as Verification
import myges as MyGes
import reload_session as ReloadSession

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def doRequest() :
  request = Request.start()

  return request

async def sessionValidity(channel) :
  request = doRequest()
  status = Verification.getSessionValidity(request)
  print("status = " + str(status))

  while status == -1 :
    print('await channel.send("❌ Erreur de session")')
    print('await channel.send("⏳ Regénération de la session")')
    ReloadSession.start()
    request = doRequest()
    status = Verification.getSessionValidity(request)

  print('await channel.send("✅ Session valide")')

@bot.event
async def on_ready():
  task_loop.start()
  print("Conection Ok!")

@tasks.loop(hours=168)
async def task_loop():
  channel = bot.get_channel(1053333090908520541)
  await sessionValidity(channel)
  print('Check planning')
  request = doRequest()
  message = MyGes.start(request)
  print(message)
  # await channel.send(message)
  print('End !')

@bot.command(name='planning')
async def getPlanning(ctx):
  request = doRequest()
  message = MyGes.start(request)
  await ctx.send(message)
  print('End !')

@bot.command(name='clear')
async def clear(ctx, amount=10):
  await ctx.channel.purge(amount)

bot.run(os.getenv("TOKEN"))
