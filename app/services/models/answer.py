

class Answer:
    def __init__(self, text: str, rating: int = 0, id: int = None):
        self.id: int = id
        self.text = text
        self.rating = rating
