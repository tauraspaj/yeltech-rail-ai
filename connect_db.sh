#!/bin/bash

# Load environment variables from .env file
set -o allexport
source "$(dirname "$0")/.env"
set +o allexport

# Connect to MySQL database
mysql -h $DB_ENDPOINT -u $DB_USERNAME -p$DB_PASSWORD
