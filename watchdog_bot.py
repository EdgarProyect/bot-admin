# C:\dev\bots\b1\watchdog_bot.py

import subprocess
import time
import os
import signal
import sys

BOT_SCRIPT = "C:\\dev\\bots\\b1\\bot.py"  # Ruta a tu bot principal
CHECK_INTERVAL = 5  # segundos entre chequeos

def find_bot_processes():
    """Busca procesos de Python que estén corriendo tu bot."""
    result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    bot_pids = []
    for line in lines:
        if "python.exe" in line and os.path.basename(BOT_SCRIPT) in line:
            parts = line.split()
            if len(parts) >= 2:
                pid = int(parts[1])
                bot_pids.append(pid)
    return bot_pids

def kill_bot_processes(pids):
    """Mata los procesos duplicados."""
    for pid in pids:
        print(f"Matiendo proceso duplicado PID={pid}")
        os.kill(pid, signal.SIGTERM)

def start_bot():
    """Arranca una nueva instancia del bot."""
    print("Arrancando bot...")
    # `creationflags=subprocess.CREATE_NEW_CONSOLE` abre otra consola
    return subprocess.Popen([sys.executable, BOT_SCRIPT], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    bot_proc = None
    while True:
        # 1. Chequea y mata duplicados
        duplicates = find_bot_processes()
        if bot_proc and bot_proc.pid in duplicates:
            duplicates.remove(bot_proc.pid)
        if duplicates:
            kill_bot_processes(duplicates)

        # 2. Si el bot murió, lo reinicia
        if not bot_proc or bot_proc.poll() is not None:
            bot_proc = start_bot()

        time.sleep(CHECK_INTERVAL)
