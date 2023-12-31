import sqlalchemy
import models as md
from sqlalchemy.orm import sessionmaker


DSN = 'postgresql://localhost:5432/publishers'
engine = sqlalchemy.create_engine(DSN)


if __name__ == '__main__':
    md.create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    publisher1 = md.Publisher(name='Буквоед')
    publisher2 = md.Publisher(name='Лабиринт')
    session.add_all([publisher1, publisher2])

    book1 = md.Book(title='Капитанская дочка', publisher=publisher1)
    book2 = md.Book(title='Капитанская дочка', publisher=publisher2)
    session.add_all([book1, book2])

    shop1 = md.Shop(name='Ромашка на Арбате')
    shop2 = md.Shop(name='Лютик на Знаменке')
    session.add_all([shop1, shop2])

    stock1 = md.Stock(book=book1, shop=shop1, count='10')
    stock2 = md.Stock(book=book2, shop=shop2, count='5')
    session.add_all([stock1, stock2])

    sale1 = md.Sale(price=100, data_sale='01.01.2023', stock=stock1, count=2)
    sale2 = md.Sale(price=50, data_sale='05.05.2022', stock=stock2, count=1)
    session.add_all([sale1, sale2])

    for c in session.query(md.Sale).all():
        print(c)

    session.commit()
    session.close()






