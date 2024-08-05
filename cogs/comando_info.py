from discord.ext import commands
import asyncio
from acciones.info import create_info_embed, handle_info_error

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def info(self, ctx):
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

async def setup(bot):
    await bot.add_cog(Info(bot))