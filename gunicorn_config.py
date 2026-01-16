# Gunicorn configuration file for Helper Bot

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5003"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Process naming
proc_name = "helper_bot"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
setproctitle = "gunicorn: helper_bot"

# Server hooks
def on_starting(server):
    print("Starting Gunicorn server...")

def on_reload(server):
    print("Reloading Gunicorn server...")

def when_ready(server):
    print("Gunicorn server is ready. Spawning workers...")

def on_exit(server):
    print("Shutting down Gunicorn server...")
