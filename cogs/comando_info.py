from discord.ext import commands
from discord.ext.commands import Bot, Context
import asyncio
from acciones.info import create_info_embed, handle_info_error

class Info(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.canal_permitido_id = 1172339507899670600  # ID del canal donde se permitirá usar el comando

    @commands.command(name="info")
    async def info(self, ctx: Context) -> None:
        if ctx.channel.id != self.canal_permitido_id:
            await ctx.send("Este comando solo se puede usar en el canal #chat_general.")
            return
        """
        Comando de Discord para mostrar información.
        """
        try:
            embed = await create_info_embed()
            if ctx.guild is not None:
                embed.title = ctx.guild.name
            response = await ctx.send(embed=embed)
            await asyncio.sleep(30)
            await response.delete()
        except Exception as e:
            await handle_info_error(ctx, e)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Info(bot))