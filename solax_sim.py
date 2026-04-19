import random
import json
import os

class SolaxSim:
    def __init__(self, mapping_file="mapping.json"):
        self.mapping_file = mapping_file
        self.mapping = self._load_mapping()

    def _load_mapping(self):
        if not os.path.exists(self.mapping_file):
            return {}
        with open(self.mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}

    def get_data(self):
        """Generuje realistické simulované dáta."""
        processed = {}
        for idx, (name, scale, unit, is_signed) in self.mapping.items():
            # Generujeme náhodné, ale uveriteľné hodnoty
            if "Voltage" in name:
                val = random.randint(2300, 2450)
            elif "Capacity" in name:
                val = random.randint(10, 100)
            elif "Grid" in name:
                val = random.randint(32000, 33000) # Simulácia exportu/importu
            elif "Temperature" in name:
                val = random.randint(20, 50)
            else:
                val = random.randint(0, 1000)

            # Prepočet na "podpísané" číslo ak treba
            if is_signed and val > 32768:
                display_val = val - 65536
            else:
                display_val = val

            processed[name] = {
                "value": round(display_val * scale, 2),
                "unit": unit,
                "raw": val
            }
        return processed