"""
Módulo para la integración de Gemini AI con Discord.
Proporciona comandos para interactuar con los modelos de IA de Gemini.
"""
import logging
from typing import List, Optional
from datetime import datetime, timezone
import io
from PIL import Image
import asyncio
from concurrent.futures import ThreadPoolExecutor

import discord
import google.generativeai as genai
from discord.ext import commands
from config.ia_config import (
    text_generation_config,
    safety_settings,
    EMBED_COLORS,
    SUPPORTED_MIME_TYPES
)
from base.database import (
    get_or_create_gemini_session,
    add_message_to_session,
    get_session_messages,
    reset_gemini_session,
    prune_old_sessions
)

# Configuración del logging solo para errores
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tiempo máximo de espera para respuestas de Gemini (en segundos)
GEMINI_TIMEOUT = 20.0

class ComandoGemini(commands.Cog):
    """Cog para manejar comandos relacionados con Gemini AI."""

    def __init__(self, bot: commands.Bot):
        """
        Inicializa el Cog de Gemini.
        
        Args:
            bot (commands.Bot): Instancia del bot de Discord
        """
        self.bot = bot
        # Aquí se usa el modelo "gemini-2.0-flash" para el procesamiento de texto
        self.text_model = genai.GenerativeModel(
            model_name="gemini-2.0-flash", 
            generation_config=text_generation_config,
            safety_settings=safety_settings
        )
        # Aquí se usa el mismo modelo "gemini-2.0-flash" para la comprensión de imágenes
        # ya que es multimodal.
        self.multimodal_model = genai.GenerativeModel(
            model_name="gemini-2.0-flash", 
            generation_config=text_generation_config,
            safety_settings=safety_settings
        )
        # Se mantiene un diccionario en memoria como caché temporal para evitar excesivas consultas a BD
        self.chat_cache = {}
        # Crear pool de hilos para operaciones bloqueantes
        self.thread_pool = ThreadPoolExecutor(max_workers=5)
        # Limpiar sesiones inactivas (opcional)
        try:
            prune_old_sessions(days_inactive=30)
            logger.info("Se han limpiado sesiones inactivas de más de 30 días")
        except Exception as e:
            logger.error(f"Error al limpiar sesiones antiguas: {e}", exc_info=True)
    
    async def cog_unload(self):
        """
        Se llama cuando el cog es descargado.
        Cierra correctamente el ThreadPoolExecutor para liberar recursos.
        """
        if self.thread_pool:
            self.thread_pool.shutdown(wait=True)
            logger.info("ThreadPoolExecutor cerrado correctamente al descargar ComandoGemini.")

    def _get_user_chat(self, user_id: int) -> genai.ChatSession:
        """
        Obtiene o crea una sesión de chat para un usuario específico.
        Ahora utiliza la base de datos para persistencia.
        
        Args:
            user_id (int): ID del usuario de Discord
            
        Returns:
            genai.ChatSession: Sesión de chat del usuario
        """
        # Si ya está en caché, la devolvemos directamente
        if user_id in self.chat_cache:
            return self.chat_cache[user_id]
            
        # Obtenemos o creamos la sesión en la base de datos
        db_session = get_or_create_gemini_session(user_id)
        
        # Recuperamos los mensajes históricos de la BD
        db_messages = get_session_messages(db_session.id, limit=20)
        
        # Convertimos los mensajes de la BD al formato que espera Gemini API
        history = []
        for msg in db_messages:
            history.append({
                "role": msg.role,
                "parts": [msg.content]
            })
        
        # Iniciamos una nueva sesión con el historial recuperado
        chat_session = self.text_model.start_chat(history=history)
        
        # Guardamos en caché para futuras consultas
        self.chat_cache[user_id] = chat_session
        
        return chat_session

    async def _chunk_and_send(self, ctx: commands.Context, text: str) -> None:
        """
        Divide un mensaje largo en trozos más pequeños y los envía secuencialmente.
        
        Args:
            ctx: Contexto del comando
            text: Texto a dividir y enviar
        """
        # Discord tiene un límite de 2000 caracteres por mensaje
        max_length = 1990  # Dejamos un pequeño margen por si acaso
        
        # Si el mensaje es corto, lo enviamos directamente
        if len(text) <= max_length:
            await ctx.send(text)
            return
        
        # Dividir el mensaje en trozos de aproximadamente max_length
        chunks = []
        for i in range(0, len(text), max_length):
            chunk = text[i:i + max_length]
            chunks.append(chunk)
        
        # Enviar cada trozo como un mensaje separado
        for i, chunk in enumerate(chunks):
            # Añadir indicador de continuación si no es el último trozo
            if i < len(chunks) - 1:
                chunk += " [...]"
            await ctx.send(chunk)
    
    async def _process_image(self, image_bytes: bytes):
        """
        Procesa una imagen para enviarla a Gemini.
        Redimensiona la imagen si supera los límites de tamaño.
        
        Args:
            image_bytes: Bytes de la imagen a procesar
            
        Returns:
            Image: Objeto de imagen procesado para Gemini
        """
        # Abrir la imagen con PIL
        image = Image.open(io.BytesIO(image_bytes))
        
        # Comprobar si necesitamos redimensionar la imagen
        # El modelo Gemini tiene un límite de 1024x1024 píxeles
        max_size = 1024
        if image.width > max_size or image.height > max_size:
            # Calcular la proporción para mantener el aspect ratio
            ratio = min(max_size / image.width, max_size / image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            
            # Redimensionar la imagen
            image = image.resize(new_size, Image.LANCZOS)
            
            # Convertir de nuevo a bytes
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
        
        # Usar el método directo de genai para crear una imagen desde bytes
        # Este método es más compatible con diferentes versiones
        return {"mime_type": "image/png", "data": image_bytes}

    async def _run_in_thread(self, func, *args):
        """
        Ejecuta una función en un hilo separado y con timeout.
        
        Args:
            func: La función a ejecutar
            args: Argumentos para la función
            
        Returns:
            El resultado de la función
            
        Raises:
            asyncio.TimeoutError: Si la función tarda más del timeout definido
        """
        # Usamos loop.run_in_executor para ejecutar la función en un hilo separado
        loop = asyncio.get_event_loop()
        try:
            return await asyncio.wait_for(
                loop.run_in_executor(self.thread_pool, func, *args),
                timeout=GEMINI_TIMEOUT
            )
        except asyncio.TimeoutError:
            logger.warning(f"Timeout al ejecutar función {func.__name__}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al ejecutar {func.__name__} en un hilo separado: {e}", exc_info=True)
            raise
    
    def _prepare_spanish_prompt(self, prompt: str, is_image: bool = False) -> str:
        """
        Asegura que el prompt solicite una respuesta en español.
        
        Args:
            prompt (str): Prompt original del usuario
            is_image (bool): Si es True, utiliza un prompt predeterminado para imágenes cuando está vacío
            
        Returns:
            str: Prompt modificado para asegurar respuesta en español
        """
        if not prompt or prompt.strip() == "":
            return "Describe esta imagen en español" if is_image else "Hola, responde en español por favor."
        
        if "español" not in prompt.lower():
            return f"{prompt} (Responde en español)"
            
        return prompt

    @commands.command(name='gemini')
    async def gemini_command(self, ctx: commands.Context, *, prompt: str = ""):
        """
        Comando principal para interactuar con Gemini AI.
        Puede procesar texto y, opcionalmente, imágenes adjuntas.
        Uso: >gemini <tu pregunta> (adjunta una imagen si quieres análisis visual)
        
        Args:
            ctx (commands.Context): Contexto del comando
            prompt (str): Prompt del usuario
        """
        # Enviamos un mensaje de "pensando" con un embed profesional
        thinking_embed = discord.Embed(
            title="🧠 Procesando consulta...",
            description="**Pythonbot** está pensando tu respuesta. Por favor espera un momento.",
            color=EMBED_COLORS["default"]
        )
        thinking_message = await ctx.send(embed=thinking_embed)

        attached_image = None
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                # Comprobar si el adjunto es una imagen
                if attachment.content_type and any(mime_type in attachment.content_type for mime_type in SUPPORTED_MIME_TYPES):
                    try:
                        image_bytes = await attachment.read()
                        attached_image = await self._process_image(image_bytes)
                        break # Solo procesamos la primera imagen adjunta
                    except Exception as e:
                        logger.error(f"Error al procesar la imagen adjunta: {e}")
                        await thinking_message.delete()
                        await ctx.send("Hubo un error al procesar la imagen. Por favor, intenta de nuevo.")
                        return

        try:
            if attached_image:
                # Si hay una imagen, enviamos el prompt y la imagen al modelo multimodal
                # Aseguramos que responda en español
                prompt_es = self._prepare_spanish_prompt(prompt, is_image=True)
                
                try:
                    # Ejecutar la solicitud en un hilo separado con timeout
                    response = await self._run_in_thread(
                        self.multimodal_model.generate_content, 
                        [prompt_es, attached_image]
                    )
                    
                    # Guardar el mensaje del usuario en la BD (solo el prompt, no podemos guardar la imagen)
                    db_session = get_or_create_gemini_session(ctx.author.id)
                    add_message_to_session(db_session.id, "user", prompt_es)
                    
                    # Guardar la respuesta del modelo
                    response_text = response.text
                    add_message_to_session(db_session.id, "model", response_text)
                    
                except asyncio.TimeoutError:
                    await thinking_message.delete()
                    await ctx.send("La respuesta está tardando demasiado. Por favor, intenta con una consulta más simple o inténtalo más tarde.")
                    return
            else:
                # Si no hay imagen, usamos el chat de texto
                chat_session = self._get_user_chat(ctx.author.id)
                
                # Para texto también nos aseguramos que sea en español
                prompt_es = self._prepare_spanish_prompt(prompt)
                
                try:
                    # Ejecutar la solicitud en un hilo separado con timeout
                    response = await self._run_in_thread(
                        chat_session.send_message,
                        prompt_es
                    )
                    
                    # Guardar mensajes en la BD
                    db_session = get_or_create_gemini_session(ctx.author.id)
                    add_message_to_session(db_session.id, "user", prompt_es)
                    add_message_to_session(db_session.id, "model", response.text)
                    
                except asyncio.TimeoutError:
                    await thinking_message.delete()
                    await ctx.send("La respuesta está tardando demasiado. Por favor, intenta con una consulta más simple o inténtalo más tarde.")
                    return

            # Eliminar el mensaje de "pensando"
            await thinking_message.delete()
            
            # Enviar la respuesta, dividiendo en trozos si es necesario
            await self._chunk_and_send(ctx, response.text)
            
        except ValueError as e:
            # Manejar errores específicos de la API
            await thinking_message.delete()
            error_message = str(e).lower()
            
            if "blocked" in error_message:
                await ctx.send(
                    "Tu consulta ha sido bloqueada debido a restricciones de contenido. " +
                    "Por favor, reformula tu pregunta de manera más apropiada."
                )
            else:
                await ctx.send(
                    f"Ha ocurrido un error al procesar tu consulta: {str(e)[:100]}... " +
                    "Por favor, intenta reformular tu pregunta."
                )
        except Exception as e:
            # Manejar cualquier otro error
            logger.error(f"Error al procesar la solicitud de Gemini: {e}", exc_info=True)
            await thinking_message.delete()
            await ctx.send(
                "Ha ocurrido un error inesperado al procesar tu consulta. " +
                f"Por favor, intenta de nuevo más tarde. (Error: {str(e)[:100]})"
            )

    @commands.command(name='gemini_reset')
    async def reset_gemini_command(self, ctx: commands.Context):
        """
        Reinicia la sesión de chat con Gemini AI para el usuario.
        Uso: >gemini_reset
        
        Args:
            ctx (commands.Context): Contexto del comando
        """
        # Reiniciamos la sesión en BD
        reset_gemini_session(ctx.author.id)
        
        # Eliminamos la caché
        if ctx.author.id in self.chat_cache:
            del self.chat_cache[ctx.author.id]
            
        await ctx.send("He olvidado nuestra conversación anterior. ¡Empecemos de nuevo!")

async def setup(bot: commands.Bot):
    """
    Configura el cog de Gemini en el bot.
    
    Args:
        bot (commands.Bot): Instancia del bot
    """
    await bot.add_cog(ComandoGemini(bot))
