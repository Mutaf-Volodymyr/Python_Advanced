from sqlalchemy import create_engine, text, MetaData, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

with engine.connect() as conn:
    result = conn.execute(text('select "hallo"'))



# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'user'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column()


# metadata = MetaData()
#
# user_table = Table(
#     'users',  # название таблицы
#     metadata,  # метадата
#     Column('id', Integer, primary_key=True),  # колонки
#     # Column('category_id', Integer, ForeignKey('categories.id')),
#     Column('name', String(30), unique=True, nullable=False)  # колонки
# )
#
# print(metadata.tables)
# print(user_table.c)  # с - обращение к колонкам
# print(user_table.c.keys())
#
# metadata.create_all(engine)
# metadata.drop_all(engine)