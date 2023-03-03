import os
import platform
import random
import time

import discord
import psycopg2
from database import *
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import json
import asyncpraw
import asyncio

try:
    import config
except:
    pass

intents = discord.Intents.all()

is_windows = "windows" in platform.system().lower()

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = config.DATABASE_URL
try:
    DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
except:
    DISCORD_TOKEN = config.DISCORD_TOKEN
try:
    DISCORD_PLAYING = os.environ['DISCORD_PLAYING']
except:
    DISCORD_PLAYING = config.DISCORD_PLAYING

connection = psycopg2.connect(DATABASE_URL, sslmode='require')

db = Database(connection=connection)
bot = commands.Bot(command_prefix=';', intents=intents)

all = db.getBandcamp()
finds = []


async def hourlyTasks():
    global all
    while True:

        try:
            all = db.getBandcamp()
            print("SLEEPING FOR AN HOUR")
            await asyncio.sleep(60*60*1)

        except Exception as e:
            print(str(e))
            pass
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=DISCORD_PLAYING))
    pass

@bot.command()
async def find(ctx):
    global all
    global finds

    chc = random.choice(all)
    m = await ctx.send("{}".format(chc[2]))
    finds.append(m.id)
    await m.add_reaction("🔀")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    global finds
    global all
    if reaction.message.id in finds:
        await reaction.message.remove_reaction("🔀", user)
        chc = random.choice(all)
        await reaction.message.edit(content="{}".format(chc[2]))

async def main():
    async with bot:
        bot.loop.create_task(hourlyTasks())
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())
