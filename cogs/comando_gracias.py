import asyncio

import discord
from discord.ext import commands
from sqlalchemy.orm import Session
from table2ascii import PresetStyle
from table2ascii import table2ascii as t2a

from acciones.gracias import dar_gracias
from base.database import User, get_db


class ComandoGracias(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gracias")
    async def gracias_comando(self, ctx, member: discord.Member):
        """
        Permite a los usuarios agradecer a otros.
        """
        if ctx.channel.id != 1172339507899670600:  # Verificar que el comando se ejecuta en el canal permitido
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        if member == ctx.author:
            await ctx.send("No puedes agradecerte a ti mismo.")
            return

        db: Session = next(get_db())
        thanks_count = dar_gracias(db, str(member.id), member.name)

        # Enviar el mensaje de agradecimiento y guardar la respuesta en 'response'
        response = await ctx.send(f"{member.mention} ha recibido un agradecimiento. Total de agradecimientos: {thanks_count}")

        # Actualizar el nombre de usuario con el ranking
        copas = thanks_count // 20
        if copas > 0:
            await member.edit(nick=f"{member.name} {'🏆' * copas}")

        # Borrar los mensajes después de 40 segundos
        await asyncio.sleep(40)
        await ctx.message.delete()
        await response.delete()

    @commands.command(name="ranking")
    async def ranking_comando(self, ctx):
        """
        Muestra el ranking de los usuarios con más agradecimientos.
        """
        db: Session = next(get_db())
        users = db.query(User).order_by(User.thanks_count.desc()).limit(10).all()

        # Crear los datos del ranking para la tabla (usuario y puntaje)
        ranking_data = [["Usuario", "Agradecimientos"]]  # Encabezados de la tabla

        for user in users:
            ranking_data.append([user.username, user.thanks_count])

        # Usar table2ascii para dar formato a la tabla
        table = t2a(
            header=ranking_data[0],   # Los encabezados
            body=ranking_data[1:],    # Los datos (sin el encabezado)
            style=PresetStyle.thin_box # Se puede cambiar el estilo de la tabla si se desea
        )

        # Enviar la tabla en Discord dentro de un bloque de código
        await ctx.send(f"```\n{table}\n```")

async def setup(bot):
    await bot.add_cog(ComandoGracias(bot))
