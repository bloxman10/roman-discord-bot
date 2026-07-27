import json
import os


FILE = "data/giveaways.json"


def ensure_file():

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE):

        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "giveaways": []
                },
                f,
                indent=4
            )



def load_giveaways():

    ensure_file()

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save_giveaways(data):

    ensure_file()

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4
        )



def add_giveaway(giveaway):

    data = load_giveaways()

    data["giveaways"].append(
        giveaway
    )

    save_giveaways(
        data
    )



def get_giveaway(message_id):

    data = load_giveaways()

    for giveaway in data["giveaways"]:

        if giveaway["message_id"] == message_id:
            return giveaway

    return None



def get_active_giveaways():

    data = load_giveaways()

    return [

        giveaway

        for giveaway in data["giveaways"]

        if not giveaway["ended"]

    ]



def update_giveaway(updated_giveaway):

    data = load_giveaways()


    for index, giveaway in enumerate(data["giveaways"]):

        if giveaway["message_id"] == updated_giveaway["message_id"]:

            data["giveaways"][index] = updated_giveaway

            break


    save_giveaways(
        data
    )



def remove_giveaway(message_id):

    data = load_giveaways()


    data["giveaways"] = [

        giveaway

        for giveaway in data["giveaways"]

        if giveaway["message_id"] != message_id

    ]


    save_giveaways(
        data
    )



def end_giveaway(message_id):

    giveaway = get_giveaway(
        message_id
    )

    if not giveaway:
        return None


    giveaway["ended"] = True

    update_giveaway(
        giveaway
    )

    return giveaway