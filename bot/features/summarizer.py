import io

import discord
import openai
from discord.ext import commands


class Summarizer(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="summarizes")
    async def summarizes(self, ctx: discord.ApplicationContext,
                         channel: discord.Option(discord.TextChannel, "The channel to summarize"),
                         past_messages: discord.Option(int, "The number of previous messages to summarize"),
                         prompt: discord.Option(str,
                                                "The prompt to give to OpenAI") = "Briefly summarize the following chat conversation.",
                         suffix: discord.Option(str, "The suffix prompt") = "Summary:",
                         debug: discord.Option(bool) = False):

        assert past_messages < 200, "Keep past_messages below 200"

        msg_count = 0
        messages = ""

        async for message in channel.history(limit=past_messages):
            if message.author.id == self.bot.application_id:
                continue
            messages += f"{message.author}: {message.clean_content}\n"
            msg_count += 1

        print(messages)

        await ctx.defer()

        query = f"{prompt}\n\n{messages}\n\n{suffix} "

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0.7,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=1
        )
        print(response)

        tokens_used = response["usage"]["total_tokens"]

        embed = discord.Embed(
            fields=[discord.EmbedField("prompt", prompt, True), discord.EmbedField("suffix", suffix, True)],
            title=f"Summary of {channel}",
            description=response.choices[0].text,
            color=0xFF5733
        )

        embed.set_footer(text=f"{msg_count} messages. ({tokens_used} tokens, ${0.0200 * (tokens_used / 1000)})")
        await ctx.edit(embed=embed, files=[discord.File(io.StringIO(query), filename="raw_query.txt")] if debug else [])
