import json

import discord
import openai

from bot.config import Config
from bot.features.summarizer import Summarizer
from bot.features.voice_clear import VoiceChannelClear

keys = json.load(open("./keys.json"))
openai.api_key = keys['openai']
token = keys['discord']

intents = discord.Intents.default()
client = discord.Bot(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} ({client.application_id})')
    for guild in client.guilds:
        print(f'In guild "{guild.name}" ({guild.id})')


@client.event
async def on_guild_join(guild: discord.Guild):
    print(f'Joined guild "{guild.name}" ({guild.id})')


@client.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    await ctx.respond(f"An error occurred: ```{error}```")


config = Config("servers.json")

client.add_cog(Summarizer(client))
client.add_cog(VoiceChannelClear(client, config))

client.run(token)
