import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base  = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.INTEGER, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.INTEGER, primary_key=True)
    title = sq.Column(sq.String(length=40))
    id_publisher = sq.Column(sq.INTEGER, sq.ForeignKey('publisher.id'))
    publisher = relationship(Publisher, backref='books')

class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.INTEGER, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.INTEGER, primary_key=True)
    id_book = sq.Column(sq.INTEGER, sq.ForeignKey('book.id'))
    id_shop = sq.Column(sq.INTEGER, sq.ForeignKey('shop.id'))
    count = sq.Column(sq.INTEGER)
    book = relationship(Book, backref='stocks')
    shop = relationship(Shop, backref='stocks')

class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.INTEGER, primary_key=True)
    price = sq.Column(sq.DECIMAL(10, 2))
    data_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.INTEGER, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.INTEGER)
    stock = relationship(Stock, backref='sales')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)