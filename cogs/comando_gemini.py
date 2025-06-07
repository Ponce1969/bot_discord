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
    SUPPORTED_MIME_TYPES,
    BASE_EMBED_COLORS,
    LANGUAGE_MAP,
    GEMINI_TIMEOUT,
    MAX_HISTORY_LENGTH
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
        # Inicializar índice para rotación de colores
        self.embed_color_index = 0
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

    async def _get_user_chat_session(self, user_id: int) -> genai.ChatSession:
        """
        Obtiene o crea una sesión de chat para un usuario específico.
        Utiliza la base de datos para persistencia.
        
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
        db_messages = get_session_messages(db_session.id, limit=MAX_HISTORY_LENGTH)
        
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
        Divide un mensaje largo en trozos más pequeños y los envía como embeds con colores alternados.
        
        Args:
            ctx: Contexto del comando
            text: Texto a dividir y enviar
        """
        # Dividir el mensaje en trozos para los embeds (Discord limita a 4096 caracteres por embed)
        chunks = [text[i:i + 4096] for i in range(0, len(text), 4096)]
        
        # Enviar cada trozo como un embed separado, rotando colores
        for i, chunk in enumerate(chunks):
            # Obtener el color actual para la rotación
            current_color = BASE_EMBED_COLORS[self.embed_color_index % len(BASE_EMBED_COLORS)]
            # Incrementar el índice para el siguiente embed
            self.embed_color_index += 1
            
            embed = discord.Embed(
                description=chunk,
                color=current_color,
                timestamp=datetime.now(timezone.utc)
            )
            
            # Solo en el primer embed mostramos el pie con el autor
            if i == 0:
                embed.set_footer(
                    text=f"Solicitado por {ctx.author.display_name}",
                    icon_url=ctx.author.avatar.url if ctx.author.avatar else None
                )
                
            await ctx.send(embed=embed)
    
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
    
    def _prepare_localized_prompt(self, prompt: str, lang_code: str, is_image: bool = False) -> str:
        """
        Asegura que el prompt solicite una respuesta en el idioma especificado.
        
        Args:
            prompt (str): Prompt original del usuario
            lang_code (str): Código del idioma (ej: 'es', 'en', etc.)
            is_image (bool): Si es True, utiliza un prompt predeterminado para imágenes cuando está vacío
            
        Returns:
            str: Prompt modificado para asegurar respuesta en el idioma solicitado
        """
        # Obtener el nombre del idioma del mapa de idiomas, o español por defecto
        language_name = LANGUAGE_MAP.get(lang_code.lower(), "español")
        
        # Si no hay prompt, devolver un prompt predeterminado en el idioma solicitado
        if not prompt or prompt.strip() == "":
            if is_image:
                # Para imágenes, solicitar descripción en el idioma correspondiente
                if lang_code == "es":
                    return f"Describe esta imagen en español"
                else:
                    return f"Describe esta imagen en {language_name}" if lang_code == "es" else f"Describe this image in {language_name}"
            else:
                # Para chat de texto, saludar en el idioma correspondiente
                if lang_code == "es":
                    return "Hola, responde en español por favor."
                elif lang_code == "en":
                    return "Hello, please respond in English."
                else:
                    return f"Hello, please respond in {language_name}."
                    
        # Si ya hay un prompt, añadir instrucción sobre el idioma si no está presente ya
        if language_name.lower() not in prompt.lower():
            if lang_code == "es":
                return f"{prompt} (Responde en español)"
            elif lang_code == "en":
                return f"{prompt} (Respond in English)"
            else:
                return f"{prompt} (Respond in {language_name})"
                
        return prompt

    @commands.command(name='gemini')
    async def gemini_command(self, ctx: commands.Context, *, prompt: str = ""):
        """
        Comando principal para interactuar con Gemini AI.
        Puede procesar texto y, opcionalmente, imágenes adjuntas.
        Uso: >gemini [--lang <código>] <tu pregunta> (adjunta una imagen si quieres análisis visual)
        Ejemplo: >gemini --lang en How's the weather?
        
        Args:
            ctx (commands.Context): Contexto del comando
            prompt (str): Prompt del usuario, puede incluir --lang <código> para especificar idioma
        """
        # Extraer el parámetro de idioma si está presente
        lang_code = "es"  # Idioma por defecto: español
        
        # Buscar el parámetro --lang en el prompt
        if prompt and "--lang" in prompt.lower():
            parts = prompt.split()
            for i, part in enumerate(parts):
                if part.lower() == "--lang" and i + 1 < len(parts):
                    potential_lang = parts[i + 1].lower()
                    if potential_lang in LANGUAGE_MAP:
                        lang_code = potential_lang
                        # Eliminar --lang y el código de idioma del prompt
                        parts.pop(i)  # Eliminar --lang
                        parts.pop(i)  # Eliminar el código de idioma
                        prompt = " ".join(parts)
                        break
        
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
                # Aseguramos que responda en el idioma solicitado
                localized_prompt = self._prepare_localized_prompt(prompt, lang_code, is_image=True)
                
                try:
                    # Ejecutar la solicitud en un hilo separado con timeout
                    response = await self._run_in_thread(
                        self.multimodal_model.generate_content, 
                        [localized_prompt, attached_image]
                    )
                    
                    # Guardar el mensaje del usuario en la BD (solo el prompt, no podemos guardar la imagen)
                    db_session = get_or_create_gemini_session(ctx.author.id)
                    add_message_to_session(db_session.id, "user", localized_prompt)
                    
                    # Guardar la respuesta del modelo
                    response_text = response.text
                    add_message_to_session(db_session.id, "model", response_text)
                    
                except asyncio.TimeoutError:
                    await thinking_message.delete()
                    await ctx.send("La respuesta está tardando demasiado. Por favor, intenta con una consulta más simple o inténtalo más tarde.")
                    return
            else:
                # Si no hay imagen, usamos el chat de texto
                chat_session = await self._get_user_chat_session(ctx.author.id)
                
                # Preparamos el prompt con el idioma solicitado
                localized_prompt = self._prepare_localized_prompt(prompt, lang_code)
                
                try:
                    # Ejecutar la solicitud en un hilo separado con timeout
                    response = await self._run_in_thread(
                        chat_session.send_message,
                        localized_prompt
                    )
                    
                    # Guardar mensajes en la BD
                    db_session = get_or_create_gemini_session(ctx.author.id)
                    add_message_to_session(db_session.id, "user", localized_prompt)
                    add_message_to_session(db_session.id, "model", response.text)
                    
                except asyncio.TimeoutError:
                    await thinking_message.delete()
                    await ctx.send("La respuesta está tardando demasiado. Por favor, intenta con una consulta más simple o inténtalo más tarde.")
                    return

            # Eliminar el mensaje de "pensando"
            await thinking_message.delete()
            
            # Enviar la respuesta usando el nuevo método de embeds coloridos
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

    @commands.command(name='gemini_help')
    async def gemini_help_command(self, ctx: commands.Context):
        """
        Muestra ayuda sobre el uso del comando gemini y sus opciones.
        Uso: >gemini_help
        
        Args:
            ctx (commands.Context): Contexto del comando
        """
        # Crear un embed colorido con la información de ayuda
        help_embed = discord.Embed(
            title="🤖 Ayuda de Gemini AI",
            description="Gemini es un modelo de IA avanzado que puede responder preguntas, analizar imágenes y mantener conversaciones.",
            color=BASE_EMBED_COLORS[0]
        )
        
        # Comandos disponibles
        help_embed.add_field(
            name="📝 Comandos disponibles",
            value=(
                "**>gemini** [--lang código] *pregunta*\n"
                "Realiza una consulta a Gemini. Puedes adjuntar una imagen.\n\n"
                "**>gemini_reset**\n"
                "Reinicia tu conversación con Gemini.\n\n"
                "**>gemini_help**\n"
                "Muestra esta ayuda."
            ),
            inline=False
        )
        
        # Opciones de idioma
        languages = ", ".join([f"`{code}`" for code in LANGUAGE_MAP.keys()])
        help_embed.add_field(
            name="🌐 Idiomas soportados",
            value=(
                f"Puedes especificar el idioma de respuesta con `--lang código`.\n"
                f"Códigos disponibles: {languages}\n"
                f"Ejemplo: `>gemini --lang en What's the weather like?`"
            ),
            inline=False
        )
        
        # Consejos de uso
        help_embed.add_field(
            name="💡 Consejos",
            value=(
                "• Para análisis de imágenes, adjunta una imagen a tu mensaje.\n"
                "• Sé específico en tus preguntas para obtener mejores respuestas.\n"
                "• Si no especificas un idioma, Gemini responderá en español por defecto."
            ),
            inline=False
        )
        
        help_embed.set_footer(text="Gemini AI - Powered by Google")
        
        # Enviar el mensaje y configurarlo para que se borre después de 60 segundos
        await ctx.message.delete(delay=60)  # Borra el mensaje del usuario después de 60 segundos
        help_message = await ctx.send(embed=help_embed)
        await help_message.delete(delay=60)  # Borra la respuesta después de 60 segundos

async def setup(bot: commands.Bot):
    """
    Configura el cog de Gemini en el bot.
    
    Args:
        bot (commands.Bot): Instancia del bot
    """
    await bot.add_cog(ComandoGemini(bot))
