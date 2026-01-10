import asyncio

from discord.ext import commands

from acciones.registrarse import register
from base.database import User, get_db

# cogs/comando_register.py

class RegisterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='register')
    async def register_user(self, ctx):
        discord_id = str(ctx.author.id)
        username = str(ctx.author.name)

        # Obtener una sesión de la base de datos
        db = next(get_db())

        try:
            # Verificar si el usuario ya está en la base de datos
            existing_user = db.query(User).filter(User.discord_id == discord_id).first()
            if existing_user:
                mensaje = await ctx.send(f"El usuario {ctx.author} ya está registrado.")
                await asyncio.sleep(10)
                await mensaje.delete()
                await ctx.message.delete()
                return

            # Registrar el usuario
            user = await register(discord_id, username)

            # Agregar el usuario a la base de datos
            db.add(user)
            db.commit()

            mensaje = await ctx.send(f"Usuario {user.username} registrado con ID {user.discord_id}")
        except Exception as e:
            db.rollback()
            mensaje = await ctx.send(f"Error al registrar el usuario: {e}")
        finally:
            db.close()

        # Esperar 10 segundos antes de borrar los mensajes
        await asyncio.sleep(30)
        await mensaje.delete()
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(RegisterCog(bot))
