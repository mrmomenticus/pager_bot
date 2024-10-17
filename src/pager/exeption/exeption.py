class NotFoundError(Exception):
    def __init__(self, *args: str):
        self.args = args
        super().__init__()

    def __str__(self):
        return f"Не найдено:{', '.join(self.args)}"

class AlreadyAvailableError(Exception):
    def __str__(self):
        return "Такое уже есть!"