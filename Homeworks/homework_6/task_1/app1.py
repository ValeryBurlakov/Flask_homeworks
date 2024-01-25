from typing import List

from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, delete, insert, update

from models import UserModel
from schemas import UserInSchema, UserSchema
from database import startup, shutdown, db
from tools import get_password_hash
from asyncio import run

app1 = FastAPI(title='Seminar_6, Task 1')
app1.add_event_handler("startup", startup)
app1.add_event_handler("shutdown", shutdown)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app1.get("/users/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    """Получение списка всех пользователей: GET /users/"""
    query = select(UserModel)
    users = await db.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Нет ни одного пользователя")


@app1.get('/users/{user_id}', response_model=UserSchema)
async def get_single_user(user_id: int) -> UserSchema:
    """Получение информации о конкретном пользователе: GET /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app1.post('/users/', response_model=UserSchema)
async def create_user(user: UserInSchema) -> dict:
    """Создание нового пользователя: POST /users/"""
    hashed_password = await get_password_hash(user.password)
    user_dict = user.model_dump() #.dict()
    user_dict['password'] = hashed_password
    query = insert(UserModel).values(**user_dict)
    user_id = await db.execute(query, user_dict)
    return {**user_dict, 'id': user_id}


@app1.put('/users/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserSchema:
    """Обновление информации о пользователе: PUT /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        updated_user = user.model_dump(exclude_unset=True)#.dict()
        if 'password' in updated_user:
            updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = update(UserModel).where(UserModel.id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(UserModel).where(UserModel.id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


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

# работает этот метод, это они не починили просто
# @app1.delete("/users/{user_id}")
# async def delete_user(user_id: int):
#     query = delete(UserModel).where(UserModel.id == user_id)
#     await db.execute(query)
#     return {'message': 'User deleted'}


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
