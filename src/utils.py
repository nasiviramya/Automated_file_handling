# src/utils.py
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)   # ensure folder exists
LOG_FILE = LOG_PATH / "activity.log"

def log_activity(msg: str) -> None:
    timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
    line = f"{timestamp} - {msg}\n"
    with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
        f.write(line)
