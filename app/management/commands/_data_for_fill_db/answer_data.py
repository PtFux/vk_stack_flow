from dataclasses import dataclass
from random import choice


@dataclass
class AnswersData:
    first_main_answer = "It's "
    answers = ['easy', 'medium', 'hard', 'horrible', 'fun', 'sad', 'terrible', 'nice']
    second_main_answer = "You just have to solve the problem!"

    @classmethod
    def get_text(cls, i: int = -1) -> str:
        return f"{i}. {cls.first_main_answer} {choice(cls.answers)} {cls.second_main_answer}"
