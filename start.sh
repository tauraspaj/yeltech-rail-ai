#!/bin/bash

# Start gunicorn in the background
gunicorn -c python:configs.gunicorn run:app &

# Start the cron service
service cron start

# Tail the cron log file
tail -f /var/log/cron.log
