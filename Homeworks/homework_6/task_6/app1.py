from datetime import datetime, date
from typing import List

from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, delete, insert, update

from models import UserModel, ProductModel, OrderModel
from schemas import UserInSchema, UserSchema, ProductSchema, ProductInSchema, OrderSchema, OrderInSchema
from database import startup, shutdown, db
from tools import get_password_hash
from asyncio import run

app1 = FastAPI(title='Seminar_6, Task 1')
app1.add_event_handler("startup", startup)
app1.add_event_handler("shutdown", shutdown)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление

# =====================================users=====================================================
# 1. Чтение всех юзеров
@app1.get("/users/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    """Получение списка всех пользователей: GET /users/"""
    query = select(UserModel)
    users = await db.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Нет ни одного пользователя")


# 2. Чтение одного юзера
@app1.get('/users/{user_id}', response_model=UserSchema)
async def get_single_user(user_id: int) -> UserSchema:
    """Получение информации о конкретном пользователе: GET /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


# 3. Запись юзера
# {"id": 1, "name": "leonid", "surname": "baschenov", "email": "boss@mail.ru", "password": "1234qweG@"}
@app1.post('/users/', response_model=UserSchema)
async def create_user(user: UserInSchema) -> dict:
    """Создание нового пользователя: POST /users/"""
    hashed_password = await get_password_hash(user.password)
    user_dict = user.model_dump()  # .dict()
    user_dict['password'] = hashed_password
    query = insert(UserModel).values(**user_dict)
    user_id = await db.execute(query, user_dict)
    return {**user_dict, 'id': user_id}


# 4. Изменение юзера
@app1.put('/users/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserSchema:
    """Обновление информации о пользователе: PUT /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        updated_user = user.model_dump(exclude_unset=True)  # .dict()
        if 'password' in updated_user:
            updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = update(UserModel).where(UserModel.id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(UserModel).where(UserModel.id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


# 5. Удаление юзера
@app1.delete("/users/{user_id}")
async def delete_user(user_id: int) -> dict:
    """Удаление пользователя: DELETE /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        query = delete(UserModel).where(UserModel.id == user_id)
        await db.execute(query)
        return {'detail': f'Пользователь с id={db_user.id} удален'}
    raise HTTPException(status_code=404, detail="Пользователь не найден")
# ==========================================================================================


# ===================================products===============================================
# 6. Чтение всех товаров
@app1.get("/products/", response_model=List[ProductSchema])
async def get_all_products() -> List[ProductSchema]:
    """Получение списка всех товаров: GET /products/"""
    query = select(ProductModel)
    products = await db.fetch_all(query)
    if products:
        return products
    raise HTTPException(status_code=404, detail="Нет ни одного товара")


# 7. Чтение одного товара
@app1.get('/products/{product_id}', response_model=ProductSchema)
async def get_single_product(product_id: int) -> ProductSchema:
    """Получение информации о конкретном товаре: GET /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="товар не найден")


# 8. Запись товара
# {"id": 1, "name": "ручка", "description": "шариковая", "price": "15"}
@app1.post('/products/', response_model=ProductSchema)
async def create_user(product: ProductInSchema) -> dict:
    """Создание нового товара: POST /products/"""
    # hashed_password = await get_password_hash(user.password)
    product_dict = product.model_dump()  # .dict()
    # user_dict['password'] = hashed_password
    query = insert(ProductModel).values(**product_dict)
    product_id = await db.execute(query, product_dict)
    return {**product_dict, 'id': product_id}


# 9. Изменение товара
@app1.put('/products/{product_id}', response_model=ProductSchema)
async def update_product(product_id: int, product: ProductInSchema) -> ProductSchema:
    """Обновление информации о товаре: PUT /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        updated_product = product.model_dump(exclude_unset=True)  # .dict()
        # if 'password' in updated_user:
        #     updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = update(ProductModel).where(ProductModel.id == product_id).values(updated_product)
        await db.execute(query)
        return await db.fetch_one(select(ProductModel).where(ProductModel.id == product_id))
    raise HTTPException(status_code=404, detail="товар не найден")


# 10. Удаление товара
@app1.delete("/products/{product_id}")
async def delete_product(product_id: int) -> dict:
    """Удаление товара: DELETE /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        query = delete(ProductModel).where(ProductModel.id == product_id)
        await db.execute(query)
        return {'detail': f'Товар с id={db_product.id} удален'}
    raise HTTPException(status_code=404, detail="Товар не найден")


# ==========================================================================================


# ===================================orders=================================================
# 11. Чтение всех заказов
@app1.get("/orders/", response_model=List[OrderSchema])
async def get_all_products() -> List[OrderSchema]:
    """Получение списка всех заказов: GET /orders/"""
    query = select(OrderModel)
    orders = await db.fetch_all(query)
    if orders:
        return orders
    raise HTTPException(status_code=404, detail="Нет ни одного заказа")


# 12. Чтение одного заказа
@app1.get('/orders/{order_id}', response_model=OrderSchema)
async def get_single_order(order_id: int) -> OrderSchema:
    """Получение информации о конкретном заказе: GET /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        return db_order
    raise HTTPException(status_code=404, detail="заказ не найден")


# fields:
# id, user_id, product_id, order_date, status
# 13. создание заказа
@app1.post('/orders/', response_model=OrderSchema)
async def create_order(order: OrderInSchema) -> dict:
    """Создание нового заказа: POST /orders/"""
    order_dict = order.model_dump()  # .dict()
    order_date_with_time = datetime.now()
    order_date_without_time = order_date_with_time.date()
    order_dict['order_date'] = order_date_without_time
    query = insert(OrderModel).values(**order_dict)
    order_id = await db.execute(query, order_dict)
    return {**order_dict, 'id': order_id}


# 14. Изменение юзера
@app1.put('/orders/{order_id}', response_model=OrderSchema)
async def update_order(order_id: int, order: OrderInSchema) -> OrderSchema:
    """Обновление информации о заказе: PUT /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    db_product = await db.fetch_one(query)
    if db_product:
        updated_order = order.model_dump(exclude_unset=True)  # .dict()
        # if 'password' in updated_user:
        #     updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = update(OrderModel).where(OrderModel.id == order_id).values(updated_order)
        await db.execute(query)
        return await db.fetch_one(select(OrderModel).where(OrderModel.id == order_id))
    raise HTTPException(status_code=404, detail="заказ не найден")


# 15. Удаление товара
@app1.delete("/orders/{order_id}")
async def delete_order(order_id: int) -> dict:
    """Удаление заказа: DELETE /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        query = delete(OrderModel).where(OrderModel.id == order_id)
        await db.execute(query)
        return {'detail': f'Заказ с id={db_order.id} удален'}
    raise HTTPException(status_code=404, detail="заказ не найден")

if __name__ == '__main__':
    run(startup())


    async def virgin_db():
        query = delete(UserModel)
        await db.execute(query)
        query = insert(UserModel)
        for i in range(10):
            password = pwd_context.hash(f'password{i}')
            new_user = {"username": f"user{i}", "email": f"user{i}@mail.ru", "password": password}
            await db.execute(query, new_user)


    run(virgin_db())
