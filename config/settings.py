from pathlib import Path
import os
from dotenv import load_dotenv

#Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent

#load local .env file if exists
load_dotenv(dotenv_path=BASE_DIR / ".env.example")

#Credentials for api and endpoint
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

URL = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT = 20

#Cities
CITIES = ["Maputo", "Beira", "Inhambane", "Xai-Xai", "Nacala","Nelspruit"]
UNITS = "metric"

#File paths
DATA_DIR = BASE_DIR / "data"
EXCEL_FILE = DATA_DIR / "weather_data.xlsx"
DATABASE_PATH = DATA_DIR / "weather.db"
LOGS_PATH = BASE_DIR / "logs" /"pipeline.log"

#KEY validation
if not OPENWEATHER_API_KEY:
    raise ValueError("ERROR: API_KEY is missing")