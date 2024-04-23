

class Page:
    def __init__(self,
                 number: int,
                 title: str,
                 is_active: bool = False,
                 is_number: bool = False
                 ):
        self.number = number
        self.title = title
        self.is_active = is_active
        self.is_number = is_number
