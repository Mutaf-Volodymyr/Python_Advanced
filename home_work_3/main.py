from sqlalchemy import create_engine
from models import Category, Product, AbstractModel
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///:memory:')
AbstractModel.metadata.create_all(engine)

with Session(engine) as session, session.begin():
    category = Category(
        name='Электроника',
        description='Гаджеты и устройства'
    )
    category2 = Category(
        name='Книги',
        description='Печатные книги и электронные книги',
    )
    category3 = Category(
        name='Одежда',
        description='Одежда для мужчин и женщин',
    )

    session.add_all([category, category2, category3])

with Session(engine) as session, session.begin():
    product1 = Product(
        name='Смартфон',
        price=299.99,
        in_stock=True,
        category_id=1,
    )
    product2 = Product(
        name='Ноутбук',
        price=499.99,
        in_stock=True,
        category_id=1,
    )
    product3 = Product(
        name='Научно-фантастический роман',
        price=15.99,
        in_stock=True,
        category_id=2,
    )
    product4 = Product(
        name='Джинсы',
        price=40.50,
        in_stock=True,
        category_id=3,
    )
    product5 = Product(
        name='Футболка',
        price=20.00,
        in_stock=True,
        category_id=3,
    )

    session.add_all([product1, product2, product3, product4, product5])

with Session(engine) as session:
    categories = session.query(Category).all()
    for category in categories:
        print(category.product)
