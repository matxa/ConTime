FROM python:3.8-slim

ENV PYTHONUNBUFFERED True

# Create app directory
WORKDIR /usr/src/api
ENV CONTIME_ENV=production

# Bundle app source
COPY . .

RUN pip3 install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
