
import aiohttp


async def youtube_search(api_key, search_query, max_results=5):
    """
    Realiza una búsqueda en YouTube y devuelve los resultados.

    :param api_key: Clave de API de YouTube.
    :param search_query: Término de búsqueda.
    :param max_results: Número máximo de resultados a devolver.
    :return: Respuesta de la API de YouTube.
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "maxResults": max_results,
        "q": search_query,
        "type": "video",
        "key": api_key
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error al realizar la búsqueda en YouTube: {response.status}")
                    return None
        except Exception as e:
            print(f"Error al realizar la búsqueda en YouTube: {e}")
            return None
