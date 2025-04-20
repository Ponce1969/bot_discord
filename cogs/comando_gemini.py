"""
Módulo para la integración de Gemini AI con Discord.
Proporciona comandos para interactuar con los modelos de IA de Gemini.
"""
import logging
from typing import List, Optional
from datetime import datetime, timezone
import io
from PIL import Image

import discord
import google.generativeai as genai
from discord.ext import commands
from config.ia_config import (
    text_generation_config,
    image_generation_config,
    safety_settings,
    MAX_MESSAGE_LENGTH,
    MAX_HISTORY_LENGTH,
    EMBED_COLORS,
    SUPPORTED_MIME_TYPES
)

# Configuración del logging solo para errores
logging.basicConfig(
    level=logging.ERROR,
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
        self.text_model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=text_generation_config,
            safety_settings=safety_settings
        )
        self.image_model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",  # Actualizado al nuevo modelo
            generation_config=image_generation_config,
            safety_settings=safety_settings
        )
        self.chats = {}

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
        embed = discord.Embed(
            color=EMBED_COLORS["default"],
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        chunks = [text[i:i + 4096] for i in range(0, len(text), 4096)]
        embed.description = chunks[0]
        await ctx.send(embed=embed)

        for chunk in chunks[1:]:
            new_embed = discord.Embed(
                description=chunk,
                color=EMBED_COLORS["default"],
                timestamp=datetime.now(timezone.utc)
            )
            await ctx.send(embed=new_embed)

    async def _process_image(self, image_data: bytes) -> Image.Image:
        """
        Procesa los bytes de la imagen y la convierte a formato PIL.
        
        Args:
            image_data (bytes): Bytes de la imagen
            
        Returns:
            Image.Image: Imagen procesada
        """
        image = Image.open(io.BytesIO(image_data))
        
        # Convertir a RGB si es necesario
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")
            
        # Redimensionar si es necesario según los límites de Gemini
        width, height = image.size
        if width > 768 or height > 768:
            image.thumbnail((768, 768), Image.Resampling.LANCZOS)
            
        return image

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
                chat = self._get_user_chat(ctx.author.id)
                response = chat.send_message(prompt)
                await self._chunk_and_send(ctx, response.text)
                
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
    async def gemini_imagen(self, ctx: commands.Context, *, prompt: str = None):
        """
        Procesa una imagen adjunta con Gemini Vision.
        Uso: 
        1. Adjunta una imagen
        2. Responde a la imagen con >gemini_imagen [descripción opcional]
        
        Args:
            ctx (commands.Context): Contexto del comando
            prompt (str): Prompt opcional para la imagen
        """
        try:
            # Verificar si es una respuesta a un mensaje
            reference = ctx.message.reference
            if reference and reference.resolved:
                # Obtener el mensaje al que se está respondiendo
                original_message = reference.resolved
                if original_message.attachments:
                    attachment = original_message.attachments[0]
                else:
                    embed = discord.Embed(
                        title="❌ Error",
                        description="El mensaje al que respondes debe contener una imagen.",
                        color=EMBED_COLORS["error"]
                    )
                    await ctx.send(embed=embed)
                    return
            else:
                # Verificar si el mensaje actual tiene una imagen adjunta
                if ctx.message.attachments:
                    attachment = ctx.message.attachments[0]
                else:
                    embed = discord.Embed(
                        title="❌ Error",
                        description="Para usar este comando:\n1. Adjunta una imagen\n2. Responde a la imagen con >gemini_imagen [descripción opcional]",
                        color=EMBED_COLORS["error"]
                    )
                    await ctx.send(embed=embed)
                    return
            
            # Establecer prompt predeterminado si no se proporciona
            if prompt is None:
                prompt = "Describe esta imagen"

            # Verificar tipo MIME
            if not attachment.content_type.startswith('image/'):
                embed = discord.Embed(
                    title="❌ Error",
                    description="El archivo adjunto debe ser una imagen.",
                    color=EMBED_COLORS["error"]
                )
                await ctx.send(embed=embed)
                return

            if attachment.content_type not in SUPPORTED_MIME_TYPES:
                supported_formats = ", ".join(t.split('/')[-1].upper() for t in SUPPORTED_MIME_TYPES)
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Formato de imagen no soportado. Por favor usa: {supported_formats}",
                    color=EMBED_COLORS["error"]
                )
                await ctx.send(embed=embed)
                return

            async with ctx.typing():
                # Leer y procesar la imagen
                image_data = await attachment.read()
                processed_image = await self._process_image(image_data)
                
                # Generar contenido con la imagen procesada
                response = self.image_model.generate_content(
                    contents=[prompt, processed_image],
                    stream=True
                )
                response.resolve()
                
                await self._chunk_and_send(ctx, response.text)

        except Exception as e:
            logger.error(f"Error al procesar imagen: {str(e)}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error al procesar la imagen: {str(e)}",
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
