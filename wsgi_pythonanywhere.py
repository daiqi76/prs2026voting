# wsgi_pythonanywhere.py
# WSGI entry point template for deploying this app on PythonAnywhere.
# Copy the contents of this file into the WSGI configuration file that
# PythonAnywhere generates for you (found under the "Web" tab).
# IMPORTANT: paste only pure Python code — do NOT include any Markdown
# code fences (the ``` backtick lines).

import sys

# Path to the project directory (where app.py lives).
project_home = "/home/prs/prs2026voting"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask app object. PythonAnywhere expects it to be named "application".
from app import app as application
