from typing import List, Optional

from pydantic import BaseModel


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
    Post(id=1, title="Война и мир", body="Эпическое произведение Толстого, описывающее жизнь русского общества в эпоху Наполеоновских войн."),
    Post(id=2, title="Преступление и наказание", body="Роман Достоевского о моральных и этических борьбах молодого человека, убившего старуху-ростовщицу."),
    Post(id=3, title="Мастер и Маргарита", body="Мистическая сатира Булгакова о посещении дьяволом Москвы 1930-х годов."),
    Post(id=4, title="Анна Каренина", body="Трагическая история любви аристократки Анны и красивого офицера Вронского, написанная Толстым."),
    Post(id=5, title="Братья Карамазовы", body="Философский роман Достоевского о борьбе трёх братьев за наследство отца."),
    Post(id=6, title="Евгений Онегин", body="Роман в стихах Пушкина, история о неразделённой любви и потерях."),
    Post(id=7, title="Собачье сердце", body="Сатирический роман Булгакова о попытке превратить собаку в человека.")
]
