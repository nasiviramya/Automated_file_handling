from organizer import FileOrganizer
from watcher import start_watcher

WATCH_PATH = r"C:\Users\YourName\Downloads"  # change this path

def run():
    organizer = FileOrganizer(WATCH_PATH, "config/rules.json")
    start_watcher(WATCH_PATH, organizer)

if __name__ == "__main__":
    run()
