from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserModel(Base):
    """Таблица users"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(length=100), unique=True, index=True)
    password = Column(String, nullable=False)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, surname={self.surname})'


class OrderModel(Base):
    """Таблица orders"""
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    order_date = Column(Date)
    status = Column(String)
    user = relationship("UserModel", back_populates="orders")
    product = relationship("ProductModel", back_populates="orders")

    # user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship("User")
    def __str__(self):
        return f'{self.surname} {self.name}'

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, surname={self.surname})'


class ProductModel(Base):
    """Таблица products"""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    def __str__(self):
        return f'{self.name} {self.description}'

    def __repr__(self):
        return f'Product(id={self.id}, name={self.price}, description={self.description})'


UserModel.orders = relationship("OrderModel", order_by=OrderModel.id, back_populates="user")
ProductModel.orders = relationship("OrderModel", order_by=OrderModel.id, back_populates="product")
