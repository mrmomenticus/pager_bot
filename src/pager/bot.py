from pager.configs import cfg
from aiogram import Bot, Dispatcher



class PagerBot:

    def __init__(self) -> None:
        """
        Инициализация бота.
        :param token: токен для бота
        """
        self.bot = Bot(cfg["token"])
        self.dp = Dispatcher()


    def add_routes(self, routes: list) -> None:
        """
        Добавление роутов.
        :param routes: список роутов
        """
        for route in routes:
            self.dp.include_router(route)


    def get_raw_bot(self) -> Bot:
        """
        Получение бота сырого бота.
        :return: сам бот
        """
        return self.bot


    async def start_bot(self) -> None:
        await self.dp.start_polling(self.bot)


class BotManager:
    """
    Класс для работы с ботом. Выступает в роли синглтона
    """

    def __init__(self) -> None:
        self.bot = PagerBot()


    def get_pager_bot(self) -> PagerBot:
        return self.bot
    

    async def start_bot(self) -> None:
        await self.bot.start_bot()