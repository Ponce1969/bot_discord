"""
Módulo para la integración de Gemini AI con Discord.
Proporciona comandos para interactuar con los modelos de IA de Gemini.
"""
import logging
from typing import List, Optional
from datetime import datetime, timezone

import discord
import google.generativeai as genai
from discord.ext import commands
from config.ia_config import (
    text_generation_config,
    image_generation_config,
    safety_settings,
    MAX_MESSAGE_LENGTH,
    MAX_HISTORY_LENGTH,
    EMBED_COLORS
)

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComandoGemini(commands.Cog):
    """Cog para manejar comandos relacionados con Gemini AI."""

    def __init__(self, bot: commands.Bot):
        """
        Inicializa el Cog de Gemini.
        
        Args:
            bot (commands.Bot): Instancia del bot de Discord
        """
        self.bot = bot
        # Usar el nombre correcto del modelo
        self.text_model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",  # Actualizado al nuevo modelo
            generation_config=text_generation_config,
            safety_settings=safety_settings
        )
        self.image_model = genai.GenerativeModel(
            model_name="gemini-pro-vision",  # Cambiado de gemini-1.0-pro-vision a gemini-pro-vision
            generation_config=image_generation_config,
            safety_settings=safety_settings
        )
        self.chats = {}  # Diccionario para mantener chats por usuario
        logger.info("ComandoGemini inicializado correctamente")

    def _get_user_chat(self, user_id: int) -> genai.ChatSession:
        """
        Obtiene o crea una sesión de chat para un usuario específico.
        
        Args:
            user_id (int): ID del usuario de Discord
            
        Returns:
            genai.ChatSession: Sesión de chat del usuario
        """
        if user_id not in self.chats:
            self.chats[user_id] = self.text_model.start_chat(history=[])
        return self.chats[user_id]

    async def _chunk_and_send(self, ctx: commands.Context, text: str) -> None:
        """
        Divide y envía mensajes largos en partes usando embeds.
        
        Args:
            ctx (commands.Context): Contexto del comando
            text (str): Texto a enviar
        """
        # Crear un embed para la respuesta
        embed = discord.Embed(
            color=EMBED_COLORS["default"],
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        # Dividir el texto en chunks respetando el límite de Discord para embeds
        chunks = [text[i:i + 4096] for i in range(0, len(text), 4096)]
        embed.description = chunks[0]  # Asignar el primer chunk al embed
        await ctx.send(embed=embed)  # Enviar el primer embed

        for i, chunk in enumerate(chunks[1:]):  # Iterar sobre los chunks restantes
            new_embed = discord.Embed(
                description=chunk,
                color=EMBED_COLORS["default"],
                timestamp=datetime.now(timezone.utc)
            )
            await ctx.send(embed=new_embed)  # Enviar los embeds restantes

    @commands.command(name='gemini')
    async def gemini_command(self, ctx: commands.Context, *, prompt: str):
        """
        Comando principal para interactuar con Gemini AI.
        Uso: >gemini <tu pregunta>
        
        Args:
            ctx (commands.Context): Contexto del comando
            prompt (str): Prompt del usuario
        """
        try:
            async with ctx.typing():
                logger.info(f"Procesando prompt de usuario {ctx.author.id}: {prompt[:50]}...")
                
                chat = self._get_user_chat(ctx.author.id)
                response = chat.send_message(prompt)
                
                await self._chunk_and_send(ctx, response.text)
                logger.info(f"Respuesta enviada a usuario {ctx.author.id}")
                
        except Exception as e:
            logger.error(f"Error al procesar prompt: {str(e)}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Lo siento, ocurrió un error al procesar tu solicitud: {str(e)}",
                color=EMBED_COLORS["error"]
            )
            await ctx.send(embed=embed)

    @commands.command(name='gemini_reset')
    async def gemini_reset(self, ctx: commands.Context):
        """
        Reinicia el historial de chat del usuario.
        Uso: >gemini_reset
        """
        try:
            user_id = ctx.author.id
            if user_id in self.chats:
                del self.chats[user_id]
                embed = discord.Embed(
                    title="✅ Chat Reiniciado",
                    description="Tu historial de chat ha sido reiniciado.",
                    color=EMBED_COLORS["success"]
                )
                await ctx.send(embed=embed)
                logger.info(f"Chat reiniciado para usuario {user_id}")
            else:
                embed = discord.Embed(
                    description="No hay historial de chat para reiniciar.",
                    color=EMBED_COLORS["warning"]
                )
                await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Error al reiniciar chat: {str(e)}")
            embed = discord.Embed(
                title="❌ Error",
                description="Error al reiniciar el chat.",
                color=EMBED_COLORS["error"]
            )
            await ctx.send(embed=embed)

    @commands.command(name='gemini_imagen')
    async def gemini_imagen(self, ctx: commands.Context, *, prompt: str = ""):
        """
        Procesa una imagen adjunta con Gemini Vision.
        Uso: >gemini_imagen [descripción opcional]
        
        Args:
            ctx (commands.Context): Contexto del comando
            prompt (str): Prompt opcional para la imagen
        """
        try:
            if not ctx.message.attachments:
                embed = discord.Embed(
                    title="❌ Error",
                    description="Por favor, adjunta una imagen para analizar.",
                    color=EMBED_COLORS["error"]
                )
                await ctx.send(embed=embed)
                return

            attachment = ctx.message.attachments[0]
            if not attachment.content_type.startswith('image/'):
                embed = discord.Embed(
                    title="❌ Error",
                    description="El archivo adjunto debe ser una imagen.",
                    color=EMBED_COLORS["error"]
                )
                await ctx.send(embed=embed)
                return

            async with ctx.typing():
                image_data = await attachment.read()
                response = self.image_model.generate_content([prompt, image_data] if prompt else [image_data])
                await self._chunk_and_send(ctx, response.text)
                logger.info(f"Imagen procesada para usuario {ctx.author.id}")

        except Exception as e:
            logger.error(f"Error al procesar imagen: {str(e)}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error al procesar la imagen: {str(e)}",
                color=EMBED_COLORS["error"]
            )
            await ctx.send(embed=embed)

    @commands.command(name='gemini_detectar_objetos')
    async def gemini_detectar_objetos(self, ctx: commands.Context):
        """
        Detecta objetos en una imagen y devuelve las coordenadas de los cuadros de límite.
        Uso: >gemini_detectar_objetos [imagen adjunta]
        """
        try:
            if not ctx.message.attachments:
                embed = discord.Embed(
                    title="❌ Error",
                    description="Por favor, adjunta una imagen para analizar.",
                    color=EMBED_COLORS["error"]
                )
                await ctx.send(embed=embed)
                return

            attachment = ctx.message.attachments[0]
            if not attachment.content_type.startswith('image/'):
                embed = discord.Embed(
                    title="❌ Error",
                    description="El archivo adjunto debe ser una imagen.",
                    color=EMBED_COLORS["error"]
                )
                await ctx.send(embed=embed)
                return

            async with ctx.typing():
                image_data = await attachment.read()
                prompt = (
                    "Return a bounding box for each of the objects in this image "
                    "in [ymin, xmin, ymax, xmax] format."
                )
                client = genai.Client(api_key="YOUR_API_KEY")
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[image_data, prompt]
                )
                await self._chunk_and_send(ctx, response.text)
                logger.info(f"Objetos detectados para usuario {ctx.author.id}")

        except Exception as e:
            logger.error(f"Error al detectar objetos: {str(e)}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error al detectar objetos: {str(e)}",
                color=EMBED_COLORS["error"]
            )
            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    """
    Función de configuración del Cog.
    
    Args:
        bot (commands.Bot): Instancia del bot de Discord
    """
    await bot.add_cog(ComandoGemini(bot))
    logger.info("ComandoGemini Cog añadido al bot")
