import discord
from discord.ext import commands

from bot.config import Config


class VoiceChannelClear(commands.Cog):
    def __init__(self, bot: discord.Bot, config: Config):
        self.bot = bot
        self.config = config

    @discord.slash_command(name="voice_clear")
    @discord.default_permissions(manage_channels=True)
    async def enable(self, ctx: discord.ApplicationContext, channel: discord.VoiceChannel, enable: bool):
        assert channel.type == discord.ChannelType.voice, "Can only be enabled on voice channels."

        enabled_channels = self.config.get_config(ctx.guild_id)['voice_clear']['enabled_channels']

        if enable:
            assert channel.id not in enabled_channels, "channel already enabled"
            enabled_channels.append(channel.id)
            self.config.persist()
            return await ctx.respond(content=f"Enabled clearing voice channel messages on leave for {channel.mention}.")
        else:
            assert channel.id in enabled_channels, "channel not enabled"
            enabled_channels.remove(channel.id)
            self.config.persist()
            return await ctx.respond(content=f"Disabled clearing voice channel messages on leave for {channel.mention}.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        enabled_channels = self.config.get_config(member.guild.id)['voice_clear']['enabled_channels']

        if before.channel == after.channel:
            # ignore muting, deafening, etc
            return

        if not after.channel or (before.channel and before.channel != after.channel and before.channel.id in enabled_channels):
            # member left the channel or moved to another one
            messages_to_delete = []
            async for message in before.channel.history(limit=100):
                if message.author.id == member.id:
                    messages_to_delete.append(message)
            await before.channel.delete_messages(messages_to_delete)
