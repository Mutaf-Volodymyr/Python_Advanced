from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, nullable=False)
    category_fk = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship("Category", back_populates="product", uselist=False, lazy="joined")

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price}, in_stock={self.in_stock})>"

    def __str__(self):
        return self.name


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500))
    product = relationship("Product", back_populates="category", uselist=True, lazy="joined")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"

    def __str__(self):
        return self.name


