import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("shout_limit")
        except Exception:
            return None
    return None

def save_config(shout_limit):
    data = {"shout_limit": shout_limit}
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)