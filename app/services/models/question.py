

class Question:
    def __init__(
            self,
            question_id: int = 0,
            title: str = "Question Title",
            text: str = "Question Text",
            tags: list = None,
            n_answers: int = 3,
            answers: list = None,
            rating: int = 0
            ):
        self.question_id = question_id
        self.title = title
        self.text = text
        self.tags = tags or []
        self.n_answers = n_answers
        self.answers = answers or []
        self.rating = rating

