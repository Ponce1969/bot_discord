# Aca implementaremos la funcion translate que traducira el texto que le pasemos a español
from translate import Translator


def translate(text: str, to_lang: str = "es") -> str:
    """
    Traduce el texto dado al idioma especificado.

    :param text: Texto a traducir.
    :param to_lang: Código del idioma al que se traducirá el texto (por defecto es español).
    :return: Texto traducido.
    """
    try:
        translator = Translator(to_lang=to_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Error al traducir: {e}"
