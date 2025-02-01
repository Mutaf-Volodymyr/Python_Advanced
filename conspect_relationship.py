from sqlalchemy import create_engine, text, MetaData, Column, Integer, String, Table, ForeignKey, insert, select, or_, \
    update, bindparam, delete, inspect
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, Session, relationship

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
Base = declarative_base()
session = Session(bind=engine, autoflush=False)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    addresses: Mapped[list["Address"]] = relationship(back_populates='user', uselist=True, lazy='select')

    def __repr__(self):
        return f'id={self.id} | User:{self.name} | age={self.age}'


class Address(Base):
    __tablename__ = 'addresses'

    email: Mapped[str] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates='addresses', uselist=False)
    user_fk = mapped_column(ForeignKey('user.id'))

    def __repr__(self):
        return f'Address: {self.email} '


Base.metadata.create_all(engine)

# способ 1
user1 = User(id=1, name='Test1', age=20)
address1 = Address(email='aaa@aaa.com')
address2 = Address(email='bbb@aaa.com')
user1.addresses.extend([address1, address2])
session.add(user1)
session.commit()

user = session.scalar(select(User))
print(user)
print(user.addresses)
