import json

class JsonHandler:
    def __init__(self):
        """Initialize JsonHandler with an empty data list."""
        self.data: list = []

    def load_json(self, filename: str) -> list:
        """Load JSON data from a file into self.data."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []
        except json.JSONDecodeError:
            raise ValueError("File is not a valid JSON")
        return self.data

    def save_json(self, filename: str) -> None:
        """Save JSON data to a file."""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def add_entry(self, entry: dict) -> None:
        """Add an entry to self.data."""
        self.data.append(entry)

    def delete_entry(self, key: str, value) -> None:
        """Delete entries from self.data where the key matches the value."""
        self.data[:] = [entry for entry in self.data if entry.get(key) != value]
