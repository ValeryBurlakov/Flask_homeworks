from datetime import date

from pydantic import EmailStr, BaseModel, Field


# 1
class UserInSchema(BaseModel):
    """Модель пользователя без id"""
    name: str = Field(..., min_length=2, max_length=25,
                      title='Задается имя пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    surname: str = Field(..., min_length=2,
                         title='Задается фамилия пользователя')
    email: EmailStr = Field(..., title='Задается email пользователя')
    password: str = Field(..., title='Задается пароль пользователя')


# 2
class UserSchema(UserInSchema):
    """Модель пользователя с id"""
    id: int


# 3
class OrderInSchema(BaseModel):
    """Модель заказа без id"""
    user_id: int = Field(default=None, title='Задаётся айди юзера')
    product_id: int = Field(default=None, title='Задаётся айди товара')
    status: str = Field(default=None, title='Статус заказа')
    order_date: date = Field(default=None, title='Дата заказа')


# 4
class OrderSchema(OrderInSchema):
    """Модель заказа с id"""
    id: int


# 5
class ProductInSchema(BaseModel):
    """Модель товара без id"""
    name: str = Field(..., min_length=2,
                      title='Задается название товара')
    description: str = Field(..., min_length=2,
                             title='Задается описание товара')
    price: int = Field(default=None, title='Задаётся цена товара')


# 6
class ProductSchema(ProductInSchema):
    """Модель товара с id"""
    id: int
