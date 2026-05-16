from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "techstartup_db")

def connect_db():
    client = MongoClient(
        "mongodb+srv://yashank:Yashank123@cluster0.xpuzwv0.mongodb.net/",
        serverSelectionTimeoutMS=60000,
        connectTimeoutMS=60000,
        socketTimeoutMS=60000,
        tlsCAFile=certifi.where()
    )
    return client[DB_NAME]

def get_col(name):
    return connect_db()[name]

if __name__ == "__main__":
    try:
        db = connect_db()
        db.command("ping")
        print(f"[SUCCESS] Connected to MongoDB >> {db.name}")
    except Exception as e:
        print(f"[FAILED] {e}")