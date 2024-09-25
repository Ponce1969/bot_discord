# desarollando el codigo listener para escuchar eventos 
from discord.ext import commands
from sqlalchemy.orm import Session
from base.database import get_db
from acciones.oyente import fuzzy_match

class OyenteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        session = next(get_db())
        try:
            user_input = message.content
            question, answer = fuzzy_match(user_input, session)
            if question and answer:
                await message.channel.send(answer)
        finally:
            session.close()

async def setup(bot):
    await bot.add_cog(OyenteCog(bot)) 