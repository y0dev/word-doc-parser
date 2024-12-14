import json

class DataSaver:
    def __init__(self, data, output_file):
        """ Initialize with data and output file path """
        self.data = data
        self.output_file = output_file

    def save_to_json(self):
        """ Save data to a JSON file """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            print(f"Data successfully saved to {self.output_file}.")
        except Exception as e:
            raise IOError(f"Failed to save data to {self.output_file}: {e}")