from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from operator import attrgetter
from pymodels import Post, Todo, todos, posts
from config import app
from auth import get_current_user


@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo):
    max_id = max(todos, key=attrgetter('id')).id
    todo.id = max_id + 1
    todos.append(todo)
    if len(todos) > 25:
        todos.pop(0)
    return todo


@app.get("/todos/", response_model=List[Todo])
async def read_todos():
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    if todo_id < 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    try:
        todo = list(filter(lambda t: t.id == todo_id , todos))[0]
        return todo
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo):
    if todo_id < 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    try:
        db_todo = list(filter(lambda t: t.id == todo_id , todos))[0]
        db_todo = {"id": todo_id, **todo.dict()}
        return db_todo
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    if todo_id < 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    try:
        todo = list(filter(lambda t: t.id == todo_id , todos))[0]
        todos = list(filter(lambda t: t.id != todo_id, todos))
        return {"detail": "Todo deleted"}
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")



@app.get('/posts', response_model=List[Post])
async def post_list(current_user: str = Depends(get_current_user)):
    return posts


@app.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: int, current_user: str = Depends(get_current_user)):
    if post_id < 0:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        post = list(filter(lambda p: p.id == post_id , posts))[0]
        return post
    except IndexError:
        raise HTTPException(status_code=404, detail="Post not found")
