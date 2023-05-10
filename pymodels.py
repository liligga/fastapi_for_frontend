from pydantic import BaseModel
from typing import List, Optional



class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False


todos: List[Todo] = [
    Todo(id=1, title="Buy groceries", description="Milk, Cheese, Pizza, Fruit", completed=False),
    Todo(id=3, title="Read book", description="Read 'A Promised Land' by Barack Obama", completed=False)
]


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    body: str


posts: List[Post] = [
    Post(id=1, title="First Post", body="This is the body of the first post."),
    Post(id=2, title="Second Post", body="This is the body of the second post.")
]