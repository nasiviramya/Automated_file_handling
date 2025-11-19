import streamlit as st
from pathlib import Path
import json
import shutil
import time
from organizer import FileOrganizer
from utils import log_activity

st.set_page_config(page_title="Auto File Organizer", layout="wide")

st.title("📁 Automated File Handler Dashboard")

st.sidebar.header("Settings")

# Folder path input
folder_path = st.sidebar.text_input(
    "Folder to Organize",
    value=str(Path.home() / "Downloads")
)

# Load rules
rules_file = "config/rules.json"
with open(rules_file, "r") as f:
    rules = json.load(f)["rules"]

st.sidebar.write("### Current Rules")
st.sidebar.json(rules)

st.write("### Actions")

# Load organizer
organizer = FileOrganizer(folder_path, rules_file)

# Manual scan button
if st.button("🧹 Organize Existing Files"):
    folder = Path(folder_path)
    for f in folder.iterdir():
        if f.is_file():
            category = organizer.organize(f)
            log_activity(f"Moved {f.name} → {category}")
    st.success("Files organized successfully!")

# Real-time monitoring switch
if "watching" not in st.session_state:
    st.session_state["watching"] = False

def watch_folder():
    st.write("Watching for new files…")
    old_files = set(Path(folder_path).iterdir())
    placeholder = st.empty()

    while st.session_state["watching"]:
        time.sleep(1)
        new_files = set(Path(folder_path).iterdir())

        created = new_files - old_files
        for file in created:
            if file.is_file():
                category = organizer.organize(file)
                log_activity(f"Auto-moved {file.name} → {category}")
                placeholder.success(f"Moved {file.name} → {category}")

        old_files = new_files

# Start/stop real-time watcher
col1, col2 = st.columns(2)
if col1.button("▶ Start Real-Time Watcher"):
    st.session_state["watching"] = True
    watch_folder()

if col2.button("⏹ Stop Watcher"):
    st.session_state["watching"] = False
    st.warning("Watcher stopped.")

# Logs section
st.write("### 📘 Logs")
try:
    with open("logs/activity.log") as f:
        st.code(f.read())
except:
    st.info("No logs available yet.")
