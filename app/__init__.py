from distutils.debug import DEBUG
from os import getenv

CONTIME_ENV = getenv("CONTIME_ENV")

if CONTIME_ENV == "production":
  API_URL="https://contime-api.iamramos.tech"
else:
  API_URL="http://localhost:5001"
