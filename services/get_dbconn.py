import os

def get_dbconn() -> str: 
    return os.getenv("DBCONN", "dbname=mukrs user=postgres password=admin")  # Default value if not set