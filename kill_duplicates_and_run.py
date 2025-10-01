# ruta: C:\dev\bots\b1\kill_duplicates_and_run_windows.py

import subprocess
import os
import sys
from time import sleep

BOT_SCRIPT_NAME = "edbot.py"  # <-- Cambia esto si tu bot tiene otro nombre

def find_bot_processes():
    """Devuelve una lista de PIDs de procesos python que ejecutan BOT_SCRIPT_NAME"""
    pids = []
    result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    for line in lines[3:]:  # Saltamos el encabezado
        if BOT_SCRIPT_NAME in line:
            parts = line.split()
            pid = int(parts[1])
            if pid != os.getpid():
                pids.append(pid)
    return pids

def kill_processes(pids):
    for pid in pids:
        print(f"Matiendo proceso duplicado: PID {pid}")
        subprocess.run(["taskkill", "/PID", str(pid), "/F"])

if __name__ == "__main__":
    duplicates = find_bot_processes()
    if duplicates:
        kill_processes(duplicates)
        sleep(1)
    print("Arrancando el bot...")
    os.execvp("python", ["python", BOT_SCRIPT_NAME])
