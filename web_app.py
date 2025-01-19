from fastapi import FastAPI

app = FastAPI()

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

class Post(BaseModel):
    id: int
    title: str
    content: str

@app.get("/users", response_model=List[User])
async def get_users():
    # Получаем пользователей из базы данных
    users = await fetch_users()

    return users

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    # Получаем пользователя из базы данных
    user = await fetch_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.post("/users", response_model=User)
async def create_user(user: User):
    # Сохраняем пользователя в базе данных
    user = await create_user(user)

    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    # Обновляем пользователя в базе данных
    user = await update_user(user_id, user)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # Удаляем пользователя из базы данных
    await delete_user(user_id)