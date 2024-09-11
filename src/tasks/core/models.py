class Task:
    def __init__(self, title: str, description: str, completed: bool = False):
        self.title = title
        self.description = description
        self.completed = completed

    def mark_as_completed(self):
        self.completed = True
