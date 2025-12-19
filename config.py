import os
from dotenv import load_dotenv
import logging

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN_DEPS_ONE = os.getenv("TOKEN_DEPS_ONE")
TOKEN_DEPS_TWO = os.getenv("TOKEN_DEPS_TWO")
TOKEN_DEPS_THREE = os.getenv("TOKEN_DEPS_THREE")
TOKEN_DEPS_FOUR = os.getenv("TOKEN_DEPS_FOUR")

host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
