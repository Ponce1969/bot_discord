# Aqui desarrollamos la funcion cafe para el bot de discord
# los tipos de cafe irian en un diccionario

# acciones/cafe.py
def cafe(tipo: str) -> str:
    cafe = {
        "1": "☕ cafe espresso",
        "2": "☕ cafe con leche",
        "3": "☕ cafe con chocolate",
        "4": "☕ cafe con whisky",
        "5": "☕ cafe con crema",
        "6": "☕ cafe con caramelo",
        "7": "☕ cafe con ron, azucar y vainilla",
    }
    return cafe.get(tipo, "☕ cafe solo")


def opciones_cafe() -> str:
    opciones = r"""
\`\`\`
Elige un tipo de café para tomar:
1. ☕ cafe espresso
2. ☕ cafe con leche
3. ☕ cafe con chocolate
4. ☕ cafe con whisky
5. ☕ cafe con crema
6. ☕ cafe con caramelo
7. ☕ cafe con ron, azucar y vainilla
Escribe el número del café que deseas.
\`\`\`
"""
    return opciones
