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

def doRequest(count) :
  request = Request.start(count)

  return request

async def sessionValidity(channel) :
  request = doRequest(0)
  status = Verification.getSessionValidity(request)
  print("status = " + str(status))

  while status == -1 :
    await channel.send("❌ Erreur de session")
    await channel.send("⏳ Regénération de la session")
    ReloadSession.start()
    request = doRequest(0)
    status = Verification.getSessionValidity(request)

  await channel.send("✅ Session valide")

@bot.event
async def on_ready():
  task_loop.start()
  print("Conection Ok!")

@tasks.loop(hours=168)
async def task_loop():
  # channel = bot.get_channel(1053333090908520541)
  # await sessionValidity(channel)
  # print('Check planning')
  # request = doRequest()
  # message = MyGes.start(request)
  # await channel.send(message)
  print('End !')

@bot.command(name='planning')
async def getPlanning(ctx, *args) :
  await sessionValidity(ctx)
  if args:
    count = int(args[0])
    print(f'Check planning +{count}')
  else:
    count = 0
    print('Check planning')
  request = doRequest(count)
  message = MyGes.start(request)
  await ctx.send(message)
  print('End !')

@bot.command(name='clear')
async def clear(ctx):
  print("Clear all msg")
  await ctx.channel.purge()

bot.run(os.getenv("TOKEN"))
