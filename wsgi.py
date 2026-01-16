"""
WSGI entry point for running Flask with Gunicorn
Only runs the Flask web application, not the Telegram bot
"""
from helper7 import app

if __name__ == "__main__":
    app.run()
