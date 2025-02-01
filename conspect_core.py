from sqlalchemy import create_engine, text, MetaData, Column, Integer, String, Table, ForeignKey, insert, select, or_, \
    update, bindparam, delete
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, Session

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

with engine.connect() as conn:
    result = conn.execute(text('select "hallo"'))

# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'user'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column()


metadata = MetaData()

user_table = Table(
    'users',  # название таблицы
    metadata,  # метадата
    Column('id', Integer, primary_key=True),  # колонки
    # Column('adress', Integer, ForeignKey('categories.id')),
    Column('name', String(30), unique=True, nullable=False)  # колонки
)

address_table = Table(
    'address',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email_address', String(30)),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
)

# print(metadata.tables)
# print(user_table.c)  # с - обращение к колонкам
# print(user_table.c.keys())
#
# metadata.create_all(engine)
# metadata.drop_all(engine)


####### CORE
metadata.create_all(engine)

stmt = insert(user_table).values(name="Test1")  # создает заготовку запроса
# INSERT INTO users (name) VALUES (?)
stmt = stmt.compile(engine)  # создает запрос. Вторым аргументом можно передать диалект
# INSERT INTO users (name) VALUES (?)

with engine.begin() as conn:
    res = conn.execute(stmt)  # производит запись в БД

# print(res.inserted_primary_key) # возвращает последний id


stmt = insert(user_table)

with engine.begin() as conn:
    conn.execute(
        stmt, [{'name': 'Test2'}, {'name': 'Test3'}])

with engine.begin() as conn:
    conn.execute(
        insert(address_table),
        [{'email_address': 'aaa@aaa.com', 'user_id': 1}, {'email_address': 'bbb@bbb.com', 'user_id': 1}])

# select
# with engine.begin() as conn:
#     result = conn.execute(
#         select(user_table).where(
#             or_(  #
#                 user_table.c.name.startswith('Test'),  # применяются строковые методы
#                 user_table.c.name.endswith('3'),  # применяются строковые методы
#             )
#         )
#
#     )
#     result = result.all()
#     print(result)  # [(1, 'Test1'), (2, 'Test2'), (3, 'Test3')]
#
# with engine.begin() as conn:
#     result = conn.execute(
#         select(user_table.c.name)
#     )
#     result = result.mappings().all()  # создает словарь
#     print(result)  # [{'name': 'Test1'}, {'name': 'Test2'}, {'name': 'Test3'}]
#
# with engine.begin() as conn:
#     result = conn.execute(
#         select(
#             (user_table.c.id),
#             (user_table.c.name + ' lalala').label('surname')
#         )
#     )
#     result = result.mappings().all()  # создает словарь
#     print(result)  # [{'surname': 'Test1 lalala'}, {'surname': 'Test2 lalala'}, {'surname': 'Test3 lalala'}]
#     print(result[0].surname)  # Test1 lalala
#     print(result[0].id)  # 1
#
# with engine.begin() as conn:
#     result = conn.execute(
#         select(user_table).
#         where(user_table.c.id > 0).
#         join_from(user_table, address_table)
#     )
#     result = result.all()  # [(1, 'Test1'), (1, 'Test1')]
#     print(result)
#
# with engine.begin() as conn:
#     result = conn.execute(
#         select(user_table).
#         join_from(user_table, address_table, user_table.c.id == address_table.c.id)
#     )
#     result = result.all()  # [(1, 'Test1'), (2, 'Test2')]
#     print(result)

# with engine.begin() as conn:
#     result = conn.execute(
#         select(user_table, address_table).
#         join(address_table).
#         order_by(user_table.c.id)
#     ).mappings().all()
#     print(result)

# UPDATE

# with engine.begin() as conn:
#     conn.execute(
#         update(user_table).where(user_table.c.id == 1).values(name='Test4')
#     )

# with engine.begin() as conn:
#     stmt = update(user_table).where(
#         user_table.c.name == bindparam("oldname")).values(name=bindparam("newname"))
#     conn.execute(
#         stmt,
#         [
#             {'oldname': 'Test1', 'newname': 'Test-1'},
#             {'oldname': 'Test2', 'newname': 'Test-2'},
#             {'oldname': 'Test3', 'newname': 'Test-3'},
#
#         ]
#     )
#     print(conn.execute(select(user_table)).all()) # [(1, 'Test-1'), (2, 'Test-2'), (3, 'Test-3')]

# with (engine.begin() as conn):
#     del_stmt = delete(user_table).where(user_table.c.id == address_table.c.user_id).where(address_table.c.email_address.startswith('aaa'))
#     print(del_stmt.compile(dialect=mysql.dialect()))

#
# with engine.begin() as conn:
#     res = conn.execute(
#         delete(user_table) # удалить где?
#         .where(user_table.c.id.in_([1, 2])) # в каком случае?
#         .returning(user_table) # показать то, что было удалено
#     ).all()
#     print(res) # [(1, 'Test1'), (2, 'Test2')]


