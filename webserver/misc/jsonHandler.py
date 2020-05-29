import json


def read_json(file: str):
    with open(f"jsonFiles/{file}", "r") as f:
        d = json.load(f)

        f.close()

    return d
