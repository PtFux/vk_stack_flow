from dataclasses import dataclass
from random import choice, randint
from typing import List


class TagsData:
    titles = [
        'python',
        'javascript',
        'php',
        'django',
        'ORM',
        'FastApy',
        'TechnoPark',
        'VK',
        'Sqlalchemy',
        'PostgreSQL',
        'Mysql'
    ]

    @classmethod
    def get_title(cls, i: int = -1) -> str:
        if i == -1:
            return choice(cls.titles)
        return f'{choice(cls.titles)}_{i}'
