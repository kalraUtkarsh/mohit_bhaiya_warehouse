import os

MONGO_URI = os.environ['DATABASE_URL']

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
REMEMBER_COOKIE_SAMESITE = 'Lax'
