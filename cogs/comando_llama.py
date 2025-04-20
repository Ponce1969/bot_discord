from discord.ext import commands
from acciones.llama import token_manager, groq_handler

class Llama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.groq_handler = groq_handler

    @commands.command(name='llama')
    async def llama(self, ctx, *, user_message: str = None):
        """Comando para interactuar con el modelo Groq."""
        if not user_message:
            await ctx.send("Hola, debes hacerme una pregunta sobre código para que pueda responder.")
            return

        try:
            # Verificar si podemos usar tokens
            if not token_manager.use_tokens():
                await ctx.send("Se ha alcanzado el límite diario de tokens. Por favor, inténtalo de nuevo mañana.")
                return

            # Obtener la respuesta del modelo Groq
            response = await self.groq_handler.get_response(user_message)

            # Crear un embed con la respuesta
            embed = self.groq_handler.create_response_embed(ctx.author.name, response)

            # Enviar el embed
            await ctx.send(embed=embed)

        except Exception as e:
            # Manejar excepciones y enviar un mensaje de error
            await ctx.send(f"Error al obtener la respuesta del modelo: {str(e)}")

async def setup(bot):
    await bot.add_cog(Llama(bot))