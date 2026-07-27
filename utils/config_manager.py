import json
import os


CONFIG_FILE = "data/config.json"


def load_config():

    if not os.path.exists(CONFIG_FILE):
        return {}

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def save_config(config):

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            config,
            file,
            indent=4,
            ensure_ascii=False
        )