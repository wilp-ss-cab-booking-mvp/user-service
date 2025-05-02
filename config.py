'''Loads values from .env file.

Makes DB URI and JWT secret available in Python.

load_dotenv() reads .env, os.getenv() pulls specific keys.
'''
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")
JWT_SECRET = os.getenv("JWT_SECRET", "default-secret")
BOOKING_SERVICE_URL = os.getenv("BOOKING_SERVICE_URL")