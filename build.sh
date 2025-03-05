#!/bin/bash
# Exit on error
set -o errexit

# Step 1: Install Dependencies
pip install -r requirements.txt

# Step 2: Collect Static Files
python manage.py collectstatic --no-input

# Step 3: Apply Database Migrations
python manage.py migrate

# Step 4: Start the Server (Optional)
python manage.py runserver