from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text,MetaData,Table
from config import SQLServerConnector


def products_decorator(func):
    def wrapper(*args, **kwargs):
        with SQLServerConnector(username='your_username', password='your_password', server='your_server', database='your_database') as connector:
            with connector.Session() as session:
                return func(session, *args, **kwargs)
    return wrapper



metadata = MetaData()

class ProductTableDefinition:
    products = Table(
        'Produtos', metadata,
        Column('cod_produto', Integer, primary_key=True, autoincrement=True),
        Column('referencia_produto', String),
        Column('pagina', String),
        Column('categoria', String),
        Column('subcategoria', String),
        Column('marca', String),
        Column('concorrente', String),
        Column('preco_concorrente', String),
        Column('jsonatributos', String),
        Column('json_imagem_atributos', String),
        Column('url_google', String),
        Column('data_atualizacao', DateTime, server_default=text('GETDATE()'))
    )
    
    
@products_decorator
def insert_product(session, **product_data):
    new_product = ProductTableDefinition.products(**product_data)
    session.add(new_product)
    session.commit()

# Uso do decorador para inserir um novo produto
insert_product(
    referencia_produto='123', pagina='example.com', categoria='Electronics',
    subcategoria='Phones', marca='Brand X', concorrente='Competitor',
    preco_concorrente='100', jsonatributos='{}', json_imagem_atributos='{}',
    url_google='google.com'
)

# Consulta de produtos
with SQLServerConnector(username='your_username', password='your_password', server='your_server', database='your_database') as connector:
    for product in connector.query_data(ProductTableDefinition.products, batch_size=500):
        print(f"Product ID: {product.cod_produto}, Reference: {product.referencia_produto}, Page: {product.pagina}, Category: {product.categoria}, Date: {product.data_atualizacao}")
