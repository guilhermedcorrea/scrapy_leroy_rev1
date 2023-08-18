from celery import Celery

app = Celery('myapp', broker='redis://localhost:6379/0')
app.config_from_object('scrapy.conf')
app.conf.update(
    result_backend='redis://localhost:6379/0',
    worker_concurrency=1  
)
