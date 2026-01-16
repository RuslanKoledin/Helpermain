# Deployment Guide

## Running the Application

### Option 1: Development Mode (Both Flask + Bot together)
```bash
python3 helper7.py
```
This runs both the Flask web interface and Telegram bot in the same process.

### Option 2: Production Mode (Separate processes)

#### Run Flask with Gunicorn:
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

#### Run Telegram Bot separately:
```bash
python3 bot.py
```

## Using systemd Services

### Flask Service (`/etc/systemd/system/helper-web.service`):
```ini
[Unit]
Description=Helper Bot Web Interface (Flask with Gunicorn)
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/helper1bezsidebar
Environment="PATH=/usr/bin:/usr/local/bin"
EnvironmentFile=/path/to/helper1bezsidebar/.env

ExecStart=/usr/local/bin/gunicorn -c gunicorn_config.py wsgi:app

Restart=always
RestartSec=10

StandardOutput=journal
StandardError=journal
SyslogIdentifier=helper-web

NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Telegram Bot Service (use existing `bot.helper.service`):
The existing `bot.helper.service` file is already configured correctly for running the bot.

### Enable and start services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable helper-web.service
sudo systemctl enable bot.helper.service
sudo systemctl start helper-web.service
sudo systemctl start bot.helper.service
```

### Check status:
```bash
sudo systemctl status helper-web.service
sudo systemctl status bot.helper.service
```

## Troubleshooting

### Error: "gunicorn conf.py doesn't exist"
- Make sure you're using `gunicorn_config.py` not `conf.py`
- Run: `gunicorn -c gunicorn_config.py wsgi:app`

### Error: "Conflict: terminated by other getUpdates request"
- Only one Telegram bot instance can run at a time
- Check for other running instances: `ps aux | grep bot.py`
- Kill other instances before starting a new one

### PostgreSQL Connection Error
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Verify database credentials in `.env` file
- Check port 5435 is accessible

## Quick Reference

- Flask runs on: `http://0.0.0.0:5003`
- Logs: `journalctl -u helper-web.service -f` or `journalctl -u bot.helper.service -f`
- Configuration: Edit `.env` file for environment variables
