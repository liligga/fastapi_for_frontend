from operator import attrgetter
from typing import List

from fastapi import Depends, HTTPException

from app.auth import get_current_user
from app.config import app
from app.pymodels import Post, Todo, posts, todos


@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo):
    """
    Для создания новой задачи
    Args:
        todo (Todo): задача
    Поля задачи:
        title (str): заголовок
        description (str): описание
        completed (bool): выполнена или нет
    """
    max_id = max(todos, key=attrgetter('id')).id
    todo.id = max_id + 1
    todos.append(todo)
    if len(todos) > 25:
        todos.pop(0)
    return todo


@app.get("/todos/", response_model=List[Todo])
async def read_todos():
    """
    Для получения списка задач
    """
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    """
    Для получения данных об одной задаче
    Args:
        todo_id (int): id задачи
    """
    if todo_id < 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    try:
        todo = list(filter(lambda t: t.id == todo_id, todos))[0]
        return todo
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo):
    """
    Для обновления задачи
    Args:
        todo_id (int): id задачи
    """
    if todo_id < 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    try:
        db_todo = list(filter(lambda t: t.id == todo_id, todos))[0]
        db_todo = {"id": todo_id, **todo.dict()}
        return db_todo
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """
    Для удаления задачи
    Args:
        todo_id (int): id задачи
    """
    if todo_id < 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    try:
        todo = list(filter(lambda t: t.id == todo_id, todos))[0]
        todos = list(filter(lambda t: t.id != todo_id, todos))
        return {"detail": "Todo deleted", "todo": todo}
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.get('/posts', response_model=List[Post])
async def post_list(current_user: str = Depends(get_current_user)):
    """Для получения списка постов"""
    return posts


@app.get("/posts/{post_id}", response_model=Post)
async def read_post(
            post_id: int,
            current_user: str = Depends(get_current_user)
        ):
    """
    Для получения одного поста по его id
    Args:
        post_id (int): id поста
    """
    if post_id < 0:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        post = list(filter(lambda p: p.id == post_id, posts))[0]
        return post
    except IndexError:
        raise HTTPException(status_code=404, detail="Post not found")
