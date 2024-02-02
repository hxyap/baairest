workers = 3
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
bind = "0.0.0.0:8000"
max_requests = 256
max_requests_jitter = 50