
FROM python:3.9-slim


WORKDIR /app


COPY /home/guilherme/teste_scrapy_rev3/celery /app


RUN pip install -r requirements.txt


CMD ["celery", "-A", "your_celery_app", "worker", "--loglevel=info"]