import os

class Config:
    os.makedirs("data", exist_ok=True)
    
    DATABASE_URL = "sqlite:///data/coursera.db"
    CSV_DATA_PATH = "data/coursera_data.csv"
    MIN_ROWS = 1000