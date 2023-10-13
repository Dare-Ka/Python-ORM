import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import create_table, Publisher, Book, Shop, Stock, Sale
import json
load_dotenv()

DSN = f'postgresql://{os.getenv("login")}:{os.getenv("password")}@localhost:5432/{os.getenv("name")}'
engine = sqlalchemy.create_engine(DSN)
create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)
for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

writer = input('Введите имя или id автора: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
if writer.isdigit():
    query = query.filter(Publisher.id == writer)
else:
    query = query.filter(Publisher.name == writer)
for title, name, price, date_sale in query:
    print(f"{title} | {name} | {price}$ | {date_sale}")

session.close()