class NotFoundError(Exception):
    """
    Ошибка поиска данных. Например: группа была не найдена в БД

    Args:
        *args: список подаваемых данных при запроса
    """

    def __init__(self, *args: str):
        self.args = args
        super().__init__()

    def __str__(self) -> str:
        return f"Таких данных не найдено: {', '.join(self.args)}"

class AlreadyAvailableError(Exception):
    def __str__(self):
        return "Такое уже есть!"