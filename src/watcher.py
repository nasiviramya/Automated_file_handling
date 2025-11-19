from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from organizer import FileOrganizer
from utils import log_activity
import time

class Handler(FileSystemEventHandler):
    def __init__(self, organizer):
        self.organizer = organizer

    def on_created(self, event):
        if not event.is_directory:
            category = self.organizer.organize(event.src_path)
            log_activity(f"Moved {event.src_path} → {category}")

def start_watcher(path, organizer):
    observer = Observer()
    observer.schedule(Handler(organizer), path, recursive=False)
    observer.start()
    print("Watching for changes... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
