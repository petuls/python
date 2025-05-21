import discord
from discord import app_commands
from discord.ext import commands
import random

class EightBallCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question!")
    @app_commands.describe(question="The question you want to ask the magic 8-ball")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "Yes",
            "No",
            "kys", # add stuff whatever u want lwk icl yeah
        ]
        answer = random.choice(responses)
        
        # Construct the message as a simple string
        message_content = f"🔥 **Magic 8-Ball**\n\n**Question:** {question}\n**Answer:** {answer}"

        # Define allowed_mentions to disable all pings
        allowed_mentions = discord.AllowedMentions(everyone=False, users=False, roles=False)
        
        # Send the message without an embed and with pings disabled
        await interaction.response.send_message(message_content, allowed_mentions=allowed_mentions)

async def setup(bot: commands.Bot):
    await bot.add_cog(EightBallCog(bot))