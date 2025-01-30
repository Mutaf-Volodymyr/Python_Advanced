from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class AbstractModel:
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Product(AbstractModel):
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)


class Category(AbstractModel):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500))

