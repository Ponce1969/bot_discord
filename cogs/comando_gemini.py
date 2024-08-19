import google.generativeai as geneai
from discord.ext import commands
from config.ia_config import text_generation_config, image_generation_config, safety_settings

text_model = geneai.GenerativeModel(model_name="gemini-pro", generation_config=text_generation_config, safety_settings=safety_settings)
image_model = geneai.GenerativeModel(model_name="gemini-pro-vision", generation_config=image_generation_config, safety_settings=safety_settings)

class ComandoGemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat = text_model.start_chat(history=[])

    @commands.command(name='gemini')  # Decorador para crear comandos
    async def gemini(self, ctx, *, string: str):
        user_message = ctx.message.content 
        respuesta_ia = self.chat.send_message(user_message)
        
        # Dividir la respuesta en partes más pequeñas si es necesario
        max_length = 2000
        response_parts = [respuesta_ia.text[i:i + max_length] for i in range(0, len(respuesta_ia.text), max_length)]

        for part in response_parts:
            await ctx.send(part)

async def setup(bot):
    await bot.add_cog(ComandoGemini(bot))