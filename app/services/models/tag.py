

class Tag:
    def __init__(self,
                 tag_id: int = 1,
                 title: str = None,
                 color: str = "danger"):
        self.tag_id = tag_id
        self.title = title
        self.color = color
        