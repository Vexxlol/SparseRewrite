from dotenv import load_dotenv

def bang():
    load_dotenv()
    return print(f"Loaded enviroment variables!")
