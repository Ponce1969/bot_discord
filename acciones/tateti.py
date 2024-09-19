# Aqui desarrollamos el juego del tateti
# usamos un tablero de 3 x 3 con discord.ui.Button
# para que los jugadores puedan interactuar con el juego
# y un sistema de turnos para que los jugadores puedan jugar

import discord
from discord.ui import Button, View
from discord import ButtonStyle

class Tateti(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.turno = 0
        self.tablero = [[None for _ in range(3)] for _ in range(3)]
        
        # Crear botones y organizarlos en un tablero de 3x3
        for i in range(3):
            for j in range(3):
                boton = Button(style=ButtonStyle.secondary, label='-', row=i, custom_id=f'{i}{j}')
                boton.callback = self.on_button_click
                self.tablero[i][j] = boton
                self.add_item(boton)

    async def on_button_click(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            jugador = '❌' if self.turno % 2 == 0 else '⭕'
            i, j = map(int, interaction.data['custom_id'])
            if self.tablero[i][j].label == '-':
                self.tablero[i][j].label = jugador
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
                    await interaction.response.edit_message(content=f'Turno de {jugador}', view=self)
            else:
                await interaction.response.send_message('Esa casilla ya está ocupada.', ephemeral=True)
        else:
            await interaction.response.send_message('No puedes jugar en el turno de tu oponente.', ephemeral=True)

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



    