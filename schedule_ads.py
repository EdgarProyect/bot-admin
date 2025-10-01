import json
import logging
from telegram.ext import ContextTypes
from ads import send_ads  # Importa la función para enviar anuncios

logger = logging.getLogger(__name__)

def schedule_ads(job_queue):
    """
    Registra un job que ejecuta send_ads cada cierto intervalo (ej: 3 horas).
    """
    job_queue.run_repeating(send_ads_job, interval=108, first=60)  # 10800 seg = 3 horas

async def send_ads_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Job que lee grupos de 'grupos.json' y envía anuncios a cada grupo usando ads.py
    """
    try:
        with open("grupos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            grupos_ids = data.get("grupos", [])
            canales_ids = data.get("canales", [])
    except FileNotFoundError:
        logger.warning("⚠️ grupos.json no encontrado. No se envían anuncios.")
        return

    # Enviar a grupos
    for gid in grupos_ids:
        try:
            await send_ads(gid, context.bot)
            logger.info(f"📢 Anuncio enviado al grupo {gid}")
        except Exception as e:
            logger.error(f"❌ Error enviando anuncio a grupo {gid}: {e}")
            
    # Enviar a canales
    for cid in canales_ids:
        try:
            await send_ads(cid, context.bot)
            logger.info(f"📢 Anuncio enviado al canal {cid}")
        except Exception as e:
            logger.error(f"❌ Error enviando anuncio a canal {cid}: {e}")
