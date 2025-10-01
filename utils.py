import random

_last_ad = None

def obtener_anuncio(ads_list):
    global _last_ad
    if not ads_list:
        return "📢 No hay anuncios disponibles."

    anuncio = random.choice(ads_list)
    while anuncio == _last_ad and len(ads_list) > 1:
        anuncio = random.choice(ads_list)

    _last_ad = anuncio
    return anuncio
