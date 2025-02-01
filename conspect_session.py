from sqlalchemy import create_engine, text, MetaData, Column, Integer, String, Table, ForeignKey, insert, select, or_, \
    update, bindparam, delete, inspect
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, Session

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
Base = declarative_base()
session = Session(bind=engine, autoflush=False)


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]

Base.metadata.create_all(engine)

# insp = inspect(user)
# print(insp.transient) # True
# print(insp.pending) # False
# print(insp.persistent) # False
# print(insp.deleted) # False
# print(insp.detached) # False


# print(insp.transient) # False
# print(insp.pending) # True
# print(insp.persistent) # False
# print(insp.deleted) # False
# print(insp.detached) # False


# print(insp.transient) # False
# print(insp.pending) # False
# print(insp.persistent) # True
# print(insp.deleted) # False
# print(insp.detached) # False

# session.add(user)
# session.flush()
# session.delete(user)
# session.flush()
# print(insp.transient) # False
# print(insp.pending) # False
# print(insp.persistent) # False
# print(insp.deleted) # True
# print(insp.detached) # False

user1 = User(id=1, name='Test1', age=30)
user2 = User(id=2, name='Test2', age=25)

session.add(user1)
session.add(user2)
session.flush()
user1.age = 20
session.flush()
