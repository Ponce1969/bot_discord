# Asocia las palabras clave con las preguntas y respuestas en la base de datos
# y responde a las preguntas del usuario si se encuentra una coincidencia.
# Este archivo es un ejemplo de cómo se puede implementar un oyente en un bot de Discord.
from discord.ext import commands

from sqlalchemy.orm import Session
from base.database import get_db
from acciones.oyente import fuzzy_match

class OyenteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keywords = {
            "bot": ["¿Qué puedes hacer?", "¿Qué hace el bot?"],
            "jugar": ["¿Dónde puedo jugar?", "¿Cómo puedo jugar?"]
            # Agrega más palabras clave y preguntas aquí
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_input = message.content.lower()
        keyword_found = False

        for keyword in self.keywords:
            if keyword in user_input:
                keyword_found = True
                break

        if not keyword_found:
            return

        session = next(get_db())
        try:
            question, answer = fuzzy_match(user_input, session)
            if question and answer:
                await message.channel.send(answer)
        finally:
            session.close()

async def setup(bot):
    await bot.add_cog(OyenteCog(bot))