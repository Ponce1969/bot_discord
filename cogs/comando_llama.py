
from discord.ext import commands
from acciones.llama import initialize_groq_client_and_model, TokenManager
from config.lla_config import GROQ_API_KEY, GROQ_MODEL


# Inicializar el gestor de tokens
token_manager = TokenManager()

class Llama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = initialize_groq_client_and_model(GROQ_API_KEY, GROQ_MODEL)

    @commands.command(name='llama')
    async def llama(self, ctx, *, user_message: str):
        """Comando para interactuar con el modelo Groq."""
        try:
            if not token_manager.use_tokens():
                await ctx.send("Se ha alcanzado el límite diario de tokens. Por favor, inténtalo de nuevo mañana.")
                return

            # Obtener la respuesta del modelo Groq
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": user_message}],
                model=self.client.model,
            ).choices[0].message.content

            # Dividir la respuesta en partes más pequeñas si es necesario
            max_length = 2000
            response_parts = [response[i:i + max_length] for i in range(0, len(response), max_length)]

            # Enviar cada parte del mensaje por separado
            for part in response_parts:
                await ctx.send(part)

        except Exception as e:
            # Manejar excepciones y enviar un mensaje de error
            await ctx.send(f"Error al obtener la respuesta del modelo: {str(e)}")

async def setup(bot):
    await bot.add_cog(Llama(bot)) 