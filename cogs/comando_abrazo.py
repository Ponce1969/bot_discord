import asyncio

from discord.ext import commands

from acciones.abrazo import abrazo_con_nombre, abrazo_nadie, me_abrazo


class Abrazo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600  # ID del canal permitido

    @commands.command(name="abrazo")
    async def abrazo(self, ctx, nombre: str = None):
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        if nombre:
            mensaje = await ctx.send(abrazo_con_nombre(ctx.author.name, nombre))
        else:
            mensaje = await ctx.send(abrazo_nadie(ctx.author.name))

        # Esperar 30 segundos antes de borrar los mensajes
        await asyncio.sleep(30)
        await mensaje.delete()
        await ctx.message.delete()

    @commands.command(name="me_abrazo")
    async def me_abrazo(self, ctx):
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return

        mensaje = await ctx.send(me_abrazo(ctx.author.name))

        # Esperar 30 segundos antes de borrar los mensajes
        await asyncio.sleep(30)
        await mensaje.delete()
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(Abrazo(bot))

