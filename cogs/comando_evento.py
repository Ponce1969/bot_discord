import asyncio

import discord
from discord.ext import commands


class EventoCog(commands.Cog):
    """Cog para manejar eventos de voz."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Verificar si el miembro se desconectó del canal de voz
        if before.channel is not None and after.channel is None:
            # Obtener el canal de texto "chat_general"
            channel = discord.utils.get(member.guild.text_channels, name="chat_general")

            if channel is not None:
                # Crear el embed
                embed = discord.Embed(
                    title="**Saliste del canal de voz!!**",
                    description=f"Gracias por tu ayuda, en el canal de voz de Gonzalo Ponce, {member.name}",
                    color=0x00FF00,  # Color verde en hexadecimal
                )

                # Enviar el mensaje embed
                response = await channel.send(embed=embed)

                # Esperar 80 segundos antes de borrar el mensaje
                await asyncio.sleep(80)
                await response.delete()


async def setup(bot):
    """Configura el Cog."""
    await bot.add_cog(EventoCog(bot))
