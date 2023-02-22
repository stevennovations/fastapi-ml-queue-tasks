
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

EXPOSE 8000

ENV PORT 8000
ENV HOST "0.0.0.0"

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt --no-cache-dir

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn main:app -c gunicorn_config.py