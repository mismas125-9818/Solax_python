import requests
import json
import os

class SolaxInverter:
    def __init__(self, ip, password, mapping_file="mapping.json"):
        self.ip = ip
        self.password = password
        self.mapping_file = mapping_file
        self.mapping = self._load_mapping()

    def _load_mapping(self):
        if not os.path.exists(self.mapping_file):
            raise FileNotFoundError(f"Chýba súbor {self.mapping_file}")
        with open(self.mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}

    def _to_signed(self, val):
        return val if val < 32768 else val - 65536

    def get_data(self):
        url = f"http://{self.ip}"
        payload = f"?optType=ReadRealTimeData&pwd={self.password}"
        try:
            response = requests.post(url, data=payload, timeout=3)
            raw_data = response.json().get("Data")
            if not raw_data:
                return None
            
            # Spracovanie do pekného slovníka
            processed = {}
            for idx, (name, scale, unit, is_signed) in self.mapping.items():
                if idx < len(raw_data):
                    val = raw_data[idx]
                    if name == "Teplota Invertora" and val > 100:
                        val -= 100
                    if is_signed:
                        val = self._to_signed(val)
                    
                    processed[name] = {
                        "value": round(val * scale, 2),
                        "unit": unit,
                        "raw": raw_data[idx]
                    }
            return processed
        except Exception:
            return None