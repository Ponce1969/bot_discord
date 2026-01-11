"""
Módulo para la integración de DeepSeek AI con Discord.
Proporciona comandos para interactuar con los modelos de IA de DeepSeek.
"""

import asyncio
import io
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import discord
from discord.ext import commands
from openai import OpenAI
from PIL import Image

from base.database import (
    add_message_to_session,
    get_or_create_gemini_session,
    get_session_messages,
    prune_old_sessions,
    reset_gemini_session,
)
from config.ia_config import (
    BASE_EMBED_COLORS,
    DEEPSEEK_TIMEOUT,
    EMBED_COLORS,
    LANGUAGE_MAP,
    MAX_HISTORY_LENGTH,
    SUPPORTED_MIME_TYPES,
)

# Configuración del logging solo para errores
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ComandoGemini(commands.Cog):
    """Cog para manejar comandos relacionados con DeepSeek AI."""

    def __init__(self, bot: commands.Bot):
        """
        Inicializa el Cog de DeepSeek.

        Args:
            bot (commands.Bot): Instancia del bot de Discord
        """
        self.bot = bot
        # Inicializar cliente DeepSeek (usa API compatible con OpenAI)
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_api_key:
            logger.error(
                "DEEPSEEK_API_KEY no está configurada en las variables de entorno"
            )
            raise ValueError("DEEPSEEK_API_KEY es requerida")

        self.client = OpenAI(
            api_key=deepseek_api_key, base_url="https://api.deepseek.com"
        )
        self.model_name = "deepseek-chat"
        # Se mantiene un diccionario en memoria como caché temporal para evitar excesivas consultas a BD
        self.chat_cache: dict[int, list] = {}
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
            logger.info(
                "ThreadPoolExecutor cerrado correctamente al descargar ComandoGemini."
            )

    async def _get_user_chat_session(self, user_id: int) -> list:
        """
        Obtiene o crea una sesión de chat para un usuario específico.
        Utiliza la base de datos para persistencia.

        Args:
            user_id (int): ID del usuario de Discord

        Returns:
            list: Historial de mensajes del usuario en formato OpenAI
        """
        # Si ya está en caché, la devolvemos directamente
        if user_id in self.chat_cache:
            return self.chat_cache[user_id]

        # Obtenemos o creamos la sesión en la base de datos
        db_session = get_or_create_gemini_session(user_id)

        # Recuperamos los mensajes históricos de la BD
        db_messages = get_session_messages(db_session.id, limit=MAX_HISTORY_LENGTH)

        # Convertimos los mensajes de la BD al formato que espera OpenAI API
        history = []
        for msg in db_messages:
            # DeepSeek usa 'user' y 'assistant' como roles
            role = "assistant" if msg.role == "model" else "user"
            history.append({"role": role, "content": msg.content})

        # Guardamos en caché para futuras consultas
        self.chat_cache[user_id] = history

        return history

    async def _chunk_and_send(self, ctx: commands.Context, text: str) -> None:
        """
        Divide un mensaje largo en trozos más pequeños y los envía como embeds con colores alternados.

        Args:
            ctx: Contexto del comando
            text: Texto a dividir y enviar
        """
        # Dividir el mensaje en trozos para los embeds (Discord limita a 4096 caracteres por embed)
        chunks = [text[i : i + 4096] for i in range(0, len(text), 4096)]

        # Enviar cada trozo como un embed separado, rotando colores
        for i, chunk in enumerate(chunks):
            # Obtener el color actual para la rotación
            current_color = BASE_EMBED_COLORS[
                self.embed_color_index % len(BASE_EMBED_COLORS)
            ]
            # Incrementar el índice para el siguiente embed
            self.embed_color_index += 1

            # Solo el último embed tendrá timestamp y footer
            if i == len(chunks) - 1:  # Último embed
                embed = discord.Embed(
                    description=chunk,
                    color=current_color,
                    timestamp=datetime.now(timezone.utc),
                )
            else:
                embed = discord.Embed(description=chunk, color=current_color)

            # Solo en el ÚLTIMO embed mostramos el pie con el autor
            if i == len(chunks) - 1:  # Último embed
                embed.set_footer(
                    text=f"Solicitado por {ctx.author.display_name}",
                    icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
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
            image = image.resize(new_size, Image.Resampling.LANCZOS)

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
        retries = 3
        for attempt in range(retries):
            try:
                return await asyncio.wait_for(
                    loop.run_in_executor(self.thread_pool, func, *args),
                    timeout=DEEPSEEK_TIMEOUT,
                )
            except asyncio.TimeoutError:
                logger.warning(
                    f"Timeout al ejecutar función {func.__name__} (intento {attempt + 1}/{retries})"
                )
                if attempt < retries - 1:
                    await asyncio.sleep(2**attempt)  # Espera exponencial
                else:
                    raise
            except Exception as e:
                error_message = str(e)
                if (
                    "429 You exceeded your current quota" in error_message
                    and attempt < retries - 1
                ):
                    logger.warning(
                        f"Error 429 (Cuota excedida) al ejecutar {func.__name__}. Reintentando en {2**attempt} segundos..."
                    )
                    await asyncio.sleep(2**attempt)  # Espera exponencial
                else:
                    logger.error(
                        f"Error inesperado al ejecutar {func.__name__} en un hilo separado: {e}",
                        exc_info=True,
                    )
                    raise

    def _prepare_localized_prompt(
        self, prompt: str, lang_code: str, is_image: bool = False
    ) -> str:
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
                    return "Describe esta imagen en español"
                else:
                    return (
                        f"Describe esta imagen en {language_name}"
                        if lang_code == "es"
                        else f"Describe this image in {language_name}"
                    )
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

    @commands.command(name="deepseek")
    async def deepseek_command(self, ctx: commands.Context, *, prompt: str = ""):
        """
        Comando principal para interactuar con DeepSeek AI.
        Puede procesar texto y, opcionalmente, imágenes adjuntas.
        Uso: >deepseek [--lang <código>] <tu pregunta> (adjunta una imagen si quieres análisis visual)
        Ejemplo: >deepseek --lang en How's the weather?

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
            title="� Procesando consulta...",
            description="**DeepSeek AI** está pensando tu respuesta. Por favor espera un momento.",
            color=EMBED_COLORS["default"],
        )
        thinking_message = await ctx.send(embed=thinking_embed)

        attached_image = None
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                # Comprobar si el adjunto es una imagen
                if attachment.content_type and any(
                    mime_type in attachment.content_type
                    for mime_type in SUPPORTED_MIME_TYPES
                ):
                    try:
                        image_bytes = await attachment.read()
                        attached_image = await self._process_image(image_bytes)
                        break  # Solo procesamos la primera imagen adjunta
                    except Exception as e:
                        logger.error(f"Error al procesar la imagen adjunta: {e}")
                        await thinking_message.delete()
                        await ctx.send(
                            "Hubo un error al procesar la imagen. Por favor, intenta de nuevo."
                        )
                        return

        try:
            if attached_image:
                # Si hay una imagen, enviamos el prompt y la imagen al modelo multimodal
                # Aseguramos que responda en el idioma solicitado
                localized_prompt = self._prepare_localized_prompt(
                    prompt, lang_code, is_image=True
                )

                try:
                    # DeepSeek soporta visión con deepseek-chat
                    # Convertir imagen a base64 para enviar
                    import base64

                    image_base64 = base64.b64encode(attached_image["data"]).decode(
                        "utf-8"
                    )

                    messages = [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": localized_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}"
                                    },
                                },
                            ],
                        }
                    ]

                    # Ejecutar la solicitud en un hilo separado con timeout
                    def call_deepseek():
                        return self.client.chat.completions.create(
                            model=self.model_name,
                            messages=messages,
                            temperature=0.9,
                            max_tokens=2000,
                        )

                    response = await self._run_in_thread(call_deepseek)

                    # Guardar el mensaje del usuario en la BD
                    db_session = get_or_create_gemini_session(ctx.author.id)
                    add_message_to_session(db_session.id, "user", localized_prompt)

                    # Guardar la respuesta del modelo
                    response_text = response.choices[0].message.content
                    add_message_to_session(db_session.id, "model", response_text)

                except asyncio.TimeoutError:
                    await thinking_message.delete()
                    await ctx.send(
                        "La respuesta está tardando demasiado. Por favor, intenta con una consulta más simple o inténtalo más tarde."
                    )
                    return
            else:
                # Si no hay imagen, usamos el chat de texto
                history = await self._get_user_chat_session(ctx.author.id)

                # Preparamos el prompt con el idioma solicitado
                localized_prompt = self._prepare_localized_prompt(prompt, lang_code)

                try:
                    # Agregar el mensaje del usuario al historial
                    messages = history + [{"role": "user", "content": localized_prompt}]

                    # Ejecutar la solicitud en un hilo separado con timeout
                    def call_deepseek():
                        return self.client.chat.completions.create(
                            model=self.model_name,
                            messages=messages,
                            temperature=0.9,
                            max_tokens=2000,
                        )

                    response = await self._run_in_thread(call_deepseek)

                    # Guardar mensajes en la BD
                    db_session = get_or_create_gemini_session(ctx.author.id)
                    add_message_to_session(db_session.id, "user", localized_prompt)
                    response_text = response.choices[0].message.content
                    add_message_to_session(db_session.id, "model", response_text)

                    # Actualizar caché con la nueva respuesta
                    self.chat_cache[ctx.author.id] = messages + [
                        {"role": "assistant", "content": response_text}
                    ]

                except asyncio.TimeoutError:
                    await thinking_message.delete()
                    await ctx.send(
                        "La respuesta está tardando demasiado. Por favor, intenta con una consulta más simple o inténtalo más tarde."
                    )
                    return

            # Eliminar el mensaje de "pensando"
            await thinking_message.delete()

            # Enviar la respuesta usando el nuevo método de embeds coloridos
            await self._chunk_and_send(ctx, response_text)

        except ValueError as e:
            # Manejar errores específicos de la API
            await thinking_message.delete()
            error_message = str(e).lower()

            if "blocked" in error_message:
                await ctx.send(
                    "Tu consulta ha sido bloqueada debido a restricciones de contenido. "
                    + "Por favor, reformula tu pregunta de manera más apropiada."
                )
            else:
                await ctx.send(
                    f"Ha ocurrido un error al procesar tu consulta: {str(e)[:100]}... "
                    + "Por favor, intenta reformular tu pregunta."
                )
        except Exception as e:
            # Manejar cualquier otro error
            logger.error(
                f"Error al procesar la solicitud de Gemini: {e}", exc_info=True
            )
            await thinking_message.delete()
            await ctx.send(
                "Ha ocurrido un error inesperado al procesar tu consulta. "
                + f"Por favor, intenta de nuevo más tarde. (Error: {str(e)[:100]})"
            )

    @commands.command(name="deepseek_reset")
    async def reset_deepseek_command(self, ctx: commands.Context):
        """
        Reinicia la sesión de chat con DeepSeek AI para el usuario.
        Uso: >deepseek_reset

        Args:
            ctx (commands.Context): Contexto del comando
        """
        # Reiniciamos la sesión en BD
        reset_gemini_session(ctx.author.id)

        # Eliminamos la caché
        if ctx.author.id in self.chat_cache:
            del self.chat_cache[ctx.author.id]

        await ctx.send(
            "✨ He olvidado nuestra conversación anterior. ¡Empecemos de nuevo!"
        )

    @commands.command(name="deepseek_help")
    async def deepseek_help_command(self, ctx: commands.Context):
        """
        Muestra ayuda sobre el uso del comando deepseek y sus opciones.
        Uso: >deepseek_help

        Args:
            ctx (commands.Context): Contexto del comando
        """
        # Crear un embed colorido con la información de ayuda
        help_embed = discord.Embed(
            title="🤖 Ayuda de DeepSeek AI",
            description="DeepSeek es un modelo de IA avanzado que puede responder preguntas, analizar imágenes y mantener conversaciones en español.",
            color=BASE_EMBED_COLORS[0],
        )

        # Comandos disponibles
        help_embed.add_field(
            name="📝 Comandos disponibles",
            value=(
                "**>deepseek** [--lang código] *pregunta*\n"
                "Realiza una consulta a DeepSeek AI. Puedes adjuntar una imagen.\n\n"
                "**>deepseek_reset**\n"
                "Reinicia tu conversación con DeepSeek.\n\n"
                "**>deepseek_help**\n"
                "Muestra esta ayuda."
            ),
            inline=False,
        )

        # Opciones de idioma
        languages = ", ".join([f"`{code}`" for code in LANGUAGE_MAP.keys()])
        help_embed.add_field(
            name="🌐 Idiomas soportados",
            value=(
                f"Puedes especificar el idioma de respuesta con `--lang código`.\n"
                f"Códigos disponibles: {languages}\n"
                f"Ejemplo: `>deepseek --lang en What's the weather like?`\n"
                f"Por defecto, DeepSeek responde en español."
            ),
            inline=False,
        )

        # Consejos de uso
        help_embed.add_field(
            name="💡 Consejos",
            value=(
                "• Para análisis de imágenes, adjunta una imagen a tu mensaje.\n"
                "• Sé específico en tus preguntas para obtener mejores respuestas.\n"
                "• DeepSeek es económico y sin límites de cuota.\n"
                "• Responde perfectamente en español y otros idiomas."
            ),
            inline=False,
        )

        help_embed.set_footer(text="DeepSeek AI - Modelo avanzado de razonamiento")

        # Enviar el mensaje y configurarlo para que se borre después de 60 segundos
        await ctx.message.delete(
            delay=60
        )  # Borra el mensaje del usuario después de 60 segundos
        help_message = await ctx.send(embed=help_embed)
        await help_message.delete(delay=60)  # Borra la respuesta después de 60 segundos


async def setup(bot: commands.Bot):
    """
    Configura el cog de DeepSeek en el bot.

    Args:
        bot (commands.Bot): Instancia del bot
    """
    await bot.add_cog(ComandoGemini(bot))
