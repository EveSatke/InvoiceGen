import json

class JsonHandler:
    def __init__(self):
        """Initialize JsonHandler with an empty data list."""
        self.data: list = []

    def load_json(self, filename: str) -> list:
        """Load JSON data from a file into self.data and return it."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found. Initializing empty data.")
            self.data = [] 
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filename}.")
            self.data = []
        except IOError as e:
            print(f"Error reading file {filename}: {e}")
            self.data = []
        return self.data

    def save(self, filename: str, new_data: dict) -> None:
        """Save JSON data to the specified file."""
        self.load_json(filename)  
        self.data.append(new_data)
        self._write_to_file(filename)

    def delete_entry(self, filename: str, key: str, value: str) -> None:
        """Delete entries from self.data where the key matches the value."""
        self.load_json(filename)
        self.data[:] = [entry for entry in self.data if entry.get(key) != value]
        self._write_to_file(filename)

    def _write_to_file(self, file_path: str) -> None:
        """Write the current data to the specified file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")