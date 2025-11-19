import shutil
from pathlib import Path
import json

class FileOrganizer:
    def __init__(self, folder, rule_file):
        self.folder = Path(folder)
        with open(rule_file, "r") as f:
            self.rules = json.load(f)["rules"]

    def get_category(self, file):
        ext = file.suffix.lower()
        for category, ext_list in self.rules.items():
            if ext in ext_list:
                return category
        return "Others"

    def organize(self, file_path):
        file = Path(file_path)
        category = self.get_category(file)
        dest = self.folder / category
        dest.mkdir(exist_ok=True)
        shutil.move(str(file), dest / file.name)
        return category
