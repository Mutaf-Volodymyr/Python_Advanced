from select import select

from sqlalchemy import create_engine, update, func
from models import Category, Product, Base
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

electronics = Category(
    name='Электроника',
    description='Гаджеты и устройства'
)
book = Category(
    name='Книги',
    description='Печатные книги и электронные книги',
)
clothes = Category(
    name='Одежда',
    description='Одежда для мужчин и женщин',
)

smartphone = Product(
    name='Смартфон',
    price=299.99,
    in_stock=True,
)
laptop = Product(
    name='Ноутбук',
    price=499.99,
    in_stock=True,
)
sci_fi_roma = Product(
    name='Научно-фантастический роман',
    price=15.99,
    in_stock=True,
)
jeans = Product(
    name='Джинсы',
    price=40.50,
    in_stock=True,
)
t_shirt = Product(
    name='Футболка',
    price=20.00,
    in_stock=True,

)

# Добавьте в базу данных категории и продукты.
with Session(engine) as session:
    electronics.product.extend([laptop, smartphone])
    book.product.append(sci_fi_roma)
    clothes.product.extend([t_shirt, jeans])
    session.add_all([electronics, book, clothes])
    session.commit()

# Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены.
with Session(engine) as session:
    all_categories = session.query(Category).all()
    for category in all_categories:
        print(f'{category.name}:')
        for product in category.product:
            print(f'\t{product.name}: {product.price}$')

# Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
with Session(engine) as session:
    new_prise = 349.99
    updt_product = "Смартфон"
    prod: Product = session.query(Product).filter(Product.name == updt_product).scalar()
    if prod:
        prod.price = new_prise
        session.commit()
        print(f'Цена товара "{updt_product}" обновлена до {new_prise}$')

# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
with Session(engine) as session:
    res = session.query(
        Category.name, func.count(Product.id))\
        .join(Category)\
        .group_by(Category.name)\
        .all()
    for row in res:
        print(f'{row[0]}: {row[1]}')

# Отфильтруйте и выведите только те категории, в которых более одного продукта.
with Session(engine) as session:

    count_categories = func.count(Product.id).label('count_categories')
    res = session.query(
        Category.name, count_categories)\
        .join(Category)\
        .group_by(Category.name)\
        .having(count_categories > 1)\
        .all()
    for row in res:
        print(f'{row[0]}: {row[1]}')
