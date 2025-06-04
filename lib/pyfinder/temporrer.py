# Version 0.0.1
from pathlib import Path
from .printter import Printter
from shutil import rmtree


class Temporrer(Printter):
    def __init__(self, path: Path, verbose: bool = False):
        super().__init__(verbose=verbose)  # Inheriting from the Printter class
        self.temp = path
        self.created = False

    def create(self):
        if not self.temp.exists() and not self.created:
            self.temp.mkdir()
        if not self.temp.exists():
            raise FileNotFoundError(f"Temp was not created: {self.temp}")
        self.created = True

    def clear(self):
        if self.temp.exists() and self.created:
            try:
                rmtree(self.temp)
            except Exception as e:
                self.vprint(f"Error while clearing temp: {e}")
        self.created = False
