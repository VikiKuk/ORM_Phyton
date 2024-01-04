import sqlalchemy
import models as md
from sqlalchemy.orm import sessionmaker


DSN = 'postgresql://localhost:5432/publishers'
engine = sqlalchemy.create_engine(DSN)

def get_shop(name_for_search):
    array = (session.query(
        md.Book.title, md.Shop.name, md.Sale.price * md.Sale.count, md.Sale.data_sale
        ).select_from(md.Sale).
                 join(md.Stock).
                 join(md.Book).
                 join(md.Shop).
                 join(md.Publisher)
                )

    # array = (session.query( # only for me to understand how it works without relationship*
    #     md.Book.title, md.Shop.name, md.Sale.price * md.Sale.count, md.Sale.data_sale # Название книги, имя магазина, стоимость продажи и дату продажи
    # ).select_from(md.Shop).
    #          join(md.Stock, md.Stock.id_shop == md.Shop.id).
    #          join(md.Book, md.Book.id == md.Stock.id_book).
    #          join(md.Publisher, md.Publisher.id == md.Book.id_publisher).
    #          join(md.Sale, md.Sale.id_stock == md.Stock.id))

    if name_for_search.isdigit():
        filtered_array = array.filter(md.Publisher.id == name_for_search).all()
    else:
        filtered_array = array.filter(md.Publisher.name == name_for_search).all()
    for book, shop, amount, data in filtered_array:
        print(f"{book: <20} | {shop: <10} | {amount: <8} | {data.strftime('%d-%m-%Y')}")


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
    stock3 = md.Stock(book=book1, shop=shop2, count='5')
    session.add_all([stock1, stock2, stock3])

    sale1 = md.Sale(price=100, data_sale='01.01.2023', stock=stock1, count=2)
    sale2 = md.Sale(price=50, data_sale='05.05.2022', stock=stock2, count=1)
    sale3 = md.Sale(price=70, data_sale='10.10.2023', stock=stock3, count=5)
    session.add_all([sale1, sale2, sale3])

    name_for_search = input('Введите имя или id издательства для получения данных о продажах: ')
    get_shop(name_for_search)

    session.commit()
    session.close()










