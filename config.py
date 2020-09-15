import os

from dotenv import load_dotenv

load_dotenv()

# Telegram bot token
TOKEN = os.environ.get('TOKEN')

OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

FIVE_DAYS_FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'
CURRENT_WEATHER_DATA_URL = 'http://api.openweathermap.org/data/2.5/find'

LATITUDE = 49.844325
LONGITUDE = 24.009761
NUMBER_OF_CITIES = 20
MIN_NEEDED_WIND_SPEED = 5.5

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASEDIR, "subscriptions.sqlite3")


