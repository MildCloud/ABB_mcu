"""ABBMCU development configuration."""

import pathlib
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# Secret key for encrypting cookies
SECRET_KEY = b'\xda\xeb\xc1I\x0f6\x83"\xd94\x08\xd6\xa6\x9f\xd3P\xba\xf5\xecV\xd8/\r\xac'
SESSION_COOKIE_NAME = 'login'

MAX_CONTENT_LENGTH = 16 * 1024 * 1024