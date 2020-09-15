import logging

import peewee
import requests
from telegram.ext import CallbackContext

import config
from models import Subscriber

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start_command(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id

    logger.info(f"Start command received. Chat ID: {chat_id}")

    update.message.reply_text('Hi!')

    try:
        Subscriber.get(Subscriber.chat_id == chat_id)

    except peewee.DoesNotExist:
        logger.info(f"Storing new subscriber {chat_id} to DB")
        Subscriber(chat_id=chat_id).save()


def help_command(update, context):
    """Send a message when the command /help is issued."""
    logger.info(f"Help command received. Chat ID: {update.message.chat_id}")

    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    logger.info(f"Text received. Chat ID: {update.message.chat_id}")

    update.message.reply_text(update.message.text)


def callback_message(context: CallbackContext):
    forecast = get_wind_forecast()
    wind_forecast = ['\n'.join([f"{i['date_time']} {item['name']}: {i['wind_speed']} m/s"
                                for i in item['forecast']]) for item in forecast if item['forecast']]

    for subscriber in Subscriber.select():
        chat_id = subscriber.chat_id
        logger.info(f"Sending message to chat: {chat_id}")
        if wind_forecast:
            for item in wind_forecast:
                context.bot.send_message(chat_id=chat_id, text=item)
        else:
            context.bot.send_message(chat_id=chat_id, text='Nothing for next five days')
        # context.bot.send_message(chat_id=chat_id, text='test')


def get_cities_ids():
    payload = {
        'lat': config.LATITUDE,
        'lon': config.LONGITUDE,
        'cnt': config.NUMBER_OF_CITIES,
        'appid': config.OPEN_WEATHER_API_KEY
    }
    forecast = requests.get(config.CURRENT_WEATHER_DATA_URL, params=payload).json()['list']
    cities_ids = [item['id'] for item in forecast]

    return cities_ids


def get_wind_forecast():
    cities_ids = get_cities_ids()
    payloads = [{'id': city_id, 'appid': config.OPEN_WEATHER_API_KEY} for city_id in cities_ids]
    forecasts = [requests.get(config.FIVE_DAYS_FORECAST_URL, params=payload).json()
                 for payload in payloads]
    wind_forecast = [{'name': forecast['city']['name'], 'forecast': [{'date_time': item['dt_txt'],
                     'wind_speed': item['wind']['speed']} for item in forecast['list']
                     if item['wind']['speed'] >= config.MIN_NEEDED_WIND_SPEED]}
                     for forecast in forecasts]

    return wind_forecast
