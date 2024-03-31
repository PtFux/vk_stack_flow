import random
from dataclasses import dataclass

from django.core.paginator import Paginator


@dataclass
class Answer:
    text: str
    rating: int = 5


@dataclass
class Tag:
    tag_id: int = 1
    title: str = "Python"
    color: str = "danger"


@dataclass
class Question:
    question_id: int = 0
    title: str = "Question Title"
    text: str = "Question Text"
    tags: list[Tag] | None = None
    n_answers: int = 3
    answers: list[Answer] | None = None
    rating: int = 3


@dataclass
class User:
    is_authenticated: bool = True
    name: str = "V.P. Boyko"


@dataclass
class Member:
    user_id: int = 0
    username: str = "Polina"


@dataclass
class Page:
    number: int
    title: str
    is_active: bool = False
    is_number: bool = False


def paginate(objects_list, page_number=1, per_page=3):
    page_number = max(1, page_number)
    page_obj = Paginator(objects_list, per_page)
    number = min(page_number, page_obj.num_pages)
    page = page_obj.get_page(number)
    pages = [
        Page(
            number=p if type(p) == int else 0,
            title=str(p),
            is_active=True if p == number else False,
            is_number=True if type(p) == int else False
        ) for p in page_obj.get_elided_page_range(number, on_each_side=1, on_ends=2)
    ]
    return pages, objects_list[page.start_index() - 1:page.end_index()]


member_names = ['Mr. Freeman', 'Dr. House', 'Bender', 'Queen Victoria', 'V. Putin']
members = [
    Member(
        user_id=i,
        username=member_names[i]
    ) for i in range(len(member_names))
]

colors = ['dark', 'danger', 'success', 'info', 'warning']
titles = ['perl', 'python', 'TechnoPark', 'MySQL', 'django', 'Mail.Ru', 'PtFux', 'Firefox']
tags = [
    Tag(
        title=title,
        color=random.choice(colors)
    ) for title in titles
]

QUESTIONS = [
    Question(
        question_id=i,
        title=f"Question {i}",
        text=f"This is question number {i}",
        tags=tags[i % len(tags):(i+3) % len(tags)] if i % len(tags) < len(tags) - 3 else tags[:3],
        answers=[Answer(text="something"), Answer(text="djfky,jgmvtjjynliuj")]
    ) for i in range(100)
]