import os
import json
import logging

logger = logging.getLogger(__name__)

GRUPOS_FILE = "grupos.json"

def cargar_grupos():
    """Carga el archivo grupos.json o retorna un dict vacío si no existe."""
    if os.path.exists(GRUPOS_FILE):
        try:
            with open(GRUPOS_FILE, "r", encoding="utf-8") as f:
                grupos = json.load(f)
                logger.info(f"✅ Grupos cargados: {len(grupos)}")
                return grupos
        except Exception as e:
            logger.error(f"❌ Error al cargar grupos.json: {e}")
            return {}
    else:
        logger.warning("⚠️ grupos.json no existe. Inicializando vacío.")
        return {}

def guardar_grupos(grupos: dict):
    """Guarda el dict grupos en grupos.json"""
    try:
        with open(GRUPOS_FILE, "w", encoding="utf-8") as f:
            json.dump(grupos, f, ensure_ascii=False, indent=2)
        logger.info("💾 grupos.json guardado correctamente.")
    except Exception as e:
        logger.error(f"❌ Error al guardar grupos.json: {e}")

def guardar_grupo_si_nuevo(chat_id: int, title: str = None, chat_type: str = None):
    """
    Si el chat no está registrado, lo añade a grupos.json.
    Parámetros opcionales title y chat_type para guardar info extra.
    """
    grupos = cargar_grupos()
    key = str(chat_id)
    if key not in grupos:
        grupos[key] = {
            "title": title if title else "Desconocido",
            "type": chat_type if chat_type else "Desconocido"
        }
        guardar_grupos(grupos)
        logger.info(f"🆕 Grupo agregado: {key} - {grupos[key]}")
    else:
        logger.debug(f"ℹ️ Grupo {key} ya registrado.")

def mostrar_grupos():
    """Retorna una lista de grupos registrados para uso en comandos."""
    grupos = cargar_grupos()
    return grupos
