# wsgi_pythonanywhere.py
# WSGI entry point template for deploying this app on PythonAnywhere.
# Copy the contents of this file into the WSGI configuration file that
# PythonAnywhere generates for you (found under the "Web" tab), and replace
# YOUR_USERNAME with your actual PythonAnywhere username.

import sys

# Path to the project directory (where app.py lives).
# Replace YOUR_USERNAME with your PythonAnywhere username.
project_home = "/home/YOUR_USERNAME/prs2026voting"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask app object. PythonAnywhere expects it to be named "application".
from app import app as application
