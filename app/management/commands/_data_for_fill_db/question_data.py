from dataclasses import dataclass
from random import choice, randint


@dataclass
class QuestionsData:
    question_words = ['How', 'What', 'Who', 'Why', 'How much', 'Where']
    main_question = 'do I solve the problem?'
    main_text = 'Something is wrong!'

    @classmethod
    def get_title(cls, i: int = -1) -> str:
        return f'{i}. {choice(cls.question_words)} {cls.main_question}'

    @classmethod
    def get_text(cls, i: int = -1) -> str:
        return f'{i}. {cls.main_text}'
