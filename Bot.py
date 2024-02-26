import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import sys
import threading
import logging

from utils.bot_queue import BotQueue
from config import config

print(discord.__version__)

intents = discord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix=config.PREFIX, intents=intents)

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
bot.logger = logging.getLogger("bot")

bot.queue = BotQueue(bot)


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            bot.logger.info(f"Loaded cog {filename[:-3]}")


@bot.event
async def on_ready():
    bot.logger.info(f"Logged in as {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
    bot.logger.info(f"Discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {sys.version}")
    bot.logger.info(f"Bot prefix: {config.PREFIX}")
    bot.logger.info(f"Bot debug mode: {config.debug}")
    bot.logger.info(f"Bot debug channel: {config.debug_channel}")

from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Greedy, Context 





@bot.command()
@commands.guild_only()
@commands.is_owner()
async def all_servers(ctx: Context) -> None:
    await ctx.send(f"```{[guild.name for guild in bot.guilds]}```")


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

async def shutdown(bot):
    await bot.close()

async def start(bot):
    await load_cogs()
    try:
        await bot.start(config.TOKEN)
    except KeyboardInterrupt:
        await shutdown(bot)

def setup():
    stable_setup()

def stable_setup():
    import requests
    import time
    print("Setting up stable-diffusion...")
    while True:
        try:
            r = requests.get(config.stable_url + "/sdapi/v1/options")
            break
        except:
            time.sleep(1)
            continue
    config_req = r.json()
    print(config_req)
    config_req["directories_filename_pattern"] = "[full_prompt_hash]"

    r = requests.post(config.stable_url + "/sdapi/v1/options", json=config_req)
    print(r.json())


if sys.argv[1] == "setup":
    setup()
    
asyncio.run(start(bot))