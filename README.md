

#Iniciar projeto

scrapy startproject app

#criando um spider
scrapy genspider LeroyMerin leroymerlin.com.br

#execucao

scrapy crawl my_spider

scrapy redis-cli lpush my_spider:start_urls https://www.example.com


```Python


class SQLServerConnector:
    def __init__(self, username, password, server, database):
        self.connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
        self.engine = create_engine(self.connection_string, echo=False, pool_pre_ping=True, pool_size=20, max_overflow=5)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def create_table(self, model_class):
        self.Base.metadata.create_all(self.engine)

    def insert_data(self, model_instance):
        with self.Session() as session:
            session.add(model_instance)
            session.commit()

    def query_data(self, model_class, filter_conditions=None, batch_size=1000):
        with self.Session() as session:
            query = session.query(model_class)
            if filter_conditions:
                query = query.filter_by(**filter_conditions)
            offset = 0
            while True:
                batch = query.limit(batch_size).offset(offset).all()
                if not batch:
                    break
                for item in batch:
                    yield item
                offset += batch_size


```
<b> Integração SQLAlchemy ao Scrapy </b>



```Python

app = Celery('Crawler', broker='redis://localhost:6379/0')
app.config_from_object('scrapy.conf')
app.conf.update(
    result_backend='redis://localhost:6379/0',
    worker_concurrency=1  
)


```
<b> Integração SQLAlchemy ao Celery </b>

```Python

def products_decorator(func):
    def wrapper(*args, **kwargs):
        with SQLServerConnector(username='sa', password='123', server='localhost', database='DEV') as connector:
            with connector.Session() as session:
                return func(session, *args, **kwargs)
    return wrapper

```

<b> Decoratr para fazer conexao e update/insert/delete</b>


```Python

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"

REDIS_URL = 'redis://localhost:6379'
```

<b> Integração Redis</b>