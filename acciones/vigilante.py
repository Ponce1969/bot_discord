# acciones/vigilante.py

# Diccionario de palabras prohibidas por categoría
import unicodedata

PALABRAS_PROHIBIDAS = {
    "español": [
        "bastardo",
        "cabrón",
        "chupa pollas",
        "chingar",
        "coño",
        "culero",
        "estupida",
        "estupido",
        "mierda",
        "maricon",
        "mongolico",
        "pendeja",
        "pendejo",
        "pija",
        "puta",
        "puto",
        "zorra"
    ],
    "inglés": [
        "asshole",
        "bitch",
        "faggot",
        "fuck",
        "motherfucker",
        "prick",
        "shit",
        "whore"
    ]
    # Añade más categorías y palabras según sea necesario
}

def normalizar_texto(texto):
    """
    Normaliza el texto eliminando acentos y convirtiendo a minúsculas.

    :param texto: El texto que se va a normalizar.
    :return: El texto normalizado.
    """
    # Convertir a minúsculas
    texto = texto.lower()
    # Normalizar acentos y caracteres especiales
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto

def contiene_palabra_prohibida(mensaje):
    """
    Verifica si un mensaje contiene alguna palabra prohibida.

    :param mensaje: El mensaje que se va a verificar.
    :return: La primera palabra prohibida encontrada en el mensaje, o None si no se encuentra ninguna.
    """
    mensaje_normalizado = normalizar_texto(mensaje)  # Normalizar el mensaje
    for _categoria, palabras in PALABRAS_PROHIBIDAS.items():
        for palabra in palabras:
            if normalizar_texto(palabra) in mensaje_normalizado:  # Normalizar la palabra prohibida
                return palabra
    return None
