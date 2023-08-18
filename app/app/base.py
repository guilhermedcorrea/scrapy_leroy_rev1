
from celery import Celery

app = Celery('myapp', broker='redis://localhost:6379/0')
app.config_from_object('scrapy.conf')


@app.task
def my_celery_task(arg1, arg2):
   
    return f'Resultado da tarefa: {arg1} + {arg2}'
