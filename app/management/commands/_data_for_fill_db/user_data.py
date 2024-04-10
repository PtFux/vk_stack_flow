from dataclasses import dataclass
from random import choice, randint
from typing import List


@dataclass
class UsersData:
    default_username = 'mega_brain'
    email_domain = ['mail', 'ya', 'yandex', 'gmail', 'yahoo', 'rambler', 'bmstu']
    email_first_domain = ['ru', 'com', 'edu', 'rb']

    @classmethod
    def get_username(cls, i) -> str:
        return f'{cls.default_username}_{i}'

    @classmethod
    def get_emails(cls, i: int = -1) -> str:
        return f'user_{i}.{choice(cls.email_domain)}.{choice(cls.email_first_domain)}'

    @classmethod
    def get_passwords(cls, i: int = -1) -> str:
        return f"{str(randint(1000, 9999))}{i}{str(randint(1000, 9999))}"

