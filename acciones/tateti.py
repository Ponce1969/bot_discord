#implementamos el juego del tateti
# Importar las librerías necesarias
# jugamos con botones y vistas
# podemos elegir jugar contra otro usuario o contra el bot

import discord
from discord.ui import Button, View, Select
from discord import ButtonStyle
import random

class Tateti(View):
    def __init__(self, ctx, contra_bot=False):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.turno = 0
        self.contra_bot = contra_bot
        self.jugadores = [ctx.author.id, None]  # Lista de jugadores, inicialmente solo el autor
        self.jugador_actual = 0  # 0 es X, 1 es O
        self.tablero = [[None for _ in range(3)] for _ in range(3)]
        
        # Crear botones y organizarlos en un tablero de 3x3
        for i in range(3):
            for j in range(3):
                boton = Button(style=ButtonStyle.secondary, label='-', row=i, custom_id=f'{i}{j}')
                boton.callback = self.on_button_click
                self.tablero[i][j] = boton
                self.add_item(boton)

    async def on_button_click(self, interaction: discord.Interaction):
        jugador_id = self.jugadores[self.jugador_actual]
        
        # Si el jugador actual no está registrado, registrarlo
        if jugador_id is None:
            self.jugadores[self.jugador_actual] = interaction.user.id
            jugador_id = interaction.user.id
        
        # Verificar si es el turno del jugador que hizo clic
        if interaction.user.id != jugador_id:
            await interaction.response.send_message('No es tu turno.', ephemeral=True)
            return

        i, j = map(int, interaction.data['custom_id'])
        if self.tablero[i][j].label == '-':
            jugador = '❌' if self.jugador_actual == 0 else '⭕'
            estilo = ButtonStyle.danger if self.jugador_actual == 0 else ButtonStyle.success
            self.tablero[i][j].label = jugador
            self.tablero[i][j].style = estilo
            self.tablero[i][j].disabled = True  # Deshabilitar el botón después de ser presionado
            self.turno += 1
            # Verificar si hay un ganador
            if self.verificar_ganador(jugador):
                await interaction.response.edit_message(content=f'{jugador} ha ganado!', view=self)
                self.stop()
            elif self.turno == 9:
                await interaction.response.edit_message(content='Empate!', view=self)
                self.stop()
            else:
                # Cambiar al otro jugador
                self.jugador_actual = 1 - self.jugador_actual
                await interaction.response.edit_message(content=f'Turno de {"❌" if self.jugador_actual == 0 else "⭕"}', view=self)
                
                # Si se juega contra el bot, hacer que el bot juegue
                if self.contra_bot and self.jugador_actual == 1:
                    await self.jugada_bot(interaction)
        else:
            await interaction.response.send_message('Esa casilla ya está ocupada.', ephemeral=True)

    async def jugada_bot(self, interaction: discord.Interaction):
        # Elegir una casilla aleatoria vacía
        casillas_vacias = [(i, j) for i in range(3) for j in range(3) if self.tablero[i][j].label == '-']
        if casillas_vacias:
            i, j = random.choice(casillas_vacias)
            jugador = '⭕'
            estilo = ButtonStyle.success
            self.tablero[i][j].label = jugador
            self.tablero[i][j].style = estilo
            self.tablero[i][j].disabled = True  # Deshabilitar el botón después de ser presionado
            self.turno += 1
            # Verificar si hay un ganador
            if self.verificar_ganador(jugador):
                await interaction.message.edit(content=f'{jugador} ha ganado!', view=self)
                self.stop()
            elif self.turno == 9:
                await interaction.message.edit(content='Empate!', view=self)
                self.stop()
            else:
                # Cambiar al otro jugador
                self.jugador_actual = 1 - self.jugador_actual
                await interaction.message.edit(content=f'Turno de {"❌" if self.jugador_actual == 0 else "⭕"}', view=self)

    def verificar_ganador(self, jugador):
        # Comprobación de filas, columnas y diagonales
        for i in range(3):
            if all(self.tablero[i][j].label == jugador for j in range(3)):  # Filas
                return True
            if all(self.tablero[j][i].label == jugador for j in range(3)):  # Columnas
                return True
        if all(self.tablero[i][i].label == jugador for i in range(3)):  # Diagonal principal
            return True
        if all(self.tablero[i][2-i].label == jugador for i in range(3)):  # Diagonal inversa
            return True
        return False

class TatetiSetup(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

        select = Select(
            placeholder="Elige tu oponente",
            options=[
                discord.SelectOption(label="Otro usuario", value="usuario"),
                discord.SelectOption(label="Bot", value="bot"),
            ],
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message('No puedes elegir el oponente para este juego.', ephemeral=True)
            return

        if interaction.data['values'][0] == "usuario":
            view = Tateti(self.ctx, contra_bot=False)
        else:
            view = Tateti(self.ctx, contra_bot=True)

        await interaction.response.edit_message(content='¡Comienza el juego de tateti!', view=view)



    