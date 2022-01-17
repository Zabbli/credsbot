import asyncio
import json
import os
from urllib.request import urlopen

import discord
from discord.ext import commands

service = commands.Bot(command_prefix='!creds ')


@service.event
async def on_ready():
    print('service is ready')


@service.event
async def on_command_error(ctx, error):
    print(error)


@service.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! {round(service.latency * 1000)}ms")


async def updateBotState():
    await service.wait_until_ready()
    while not service.is_closed():
        await service.change_presence(activity=discord.Game(name=getCurrentPrice()))
        await asyncio.sleep(60)


def getCurrentPrice():
    data = json.loads(urlopen("https://api.coingecko.com/api/v3/coins/creds").read())
    num = "{:.2f}".format((float(data["market_data"]["current_price"]["usd"])))
    return f'Creds: ${num}'


service.loop.create_task(updateBotState())
service.run(os.environ.get("TOKEN"))
