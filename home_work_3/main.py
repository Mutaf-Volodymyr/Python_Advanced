from sqlalchemy import create_engine
from models import Category, Product, AbstractModel
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///:memory:')
AbstractModel.metadata.create_all(engine)

with Session(engine) as session, session.begin():
    category = Category(
        name='Category 1',
    )

    category2 = Category(
        name='Category 2',
        description='bla-bla-bla',
    )
    session.add_all([category, category2])

with Session(engine) as session, session.begin():
    product1 = Product(
        name='Product 1',
        price=25.99,
        in_stock=True,
        category_id=2,
    )
    product2 = Product(
        name='Product 2',
        price=99.99,
        in_stock=True,
        category_id=1,
    )
    session.add_all([product1, product2])

with Session(engine) as session:
    categories = session.query(Category).all()
    for category in categories:
        print(category.__dict__)

    products = session.query(Product).filter(Product.category_id == 2).all()
    for product in products:
        print(product.__dict__)
