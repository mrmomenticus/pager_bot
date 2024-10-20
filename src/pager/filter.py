
from tracemalloc import BaseFilter
from aiogram.types import Message

from pager.databases.requests.player import PlayerRequest
from pager.utils.utility import get_id_from_players


class Role(BaseFilter):

    def __init__(self, admins: list[int] = None, is_admin: bool = False) -> None:
        """
        Инициализирует объект роли.

        :param admins: список id администраторов, если None, то они будут получены из базы данных.
        :param is_admin: является ли пользователь администратором?
        :type admins: list[int]
        :type is_admin: bool
        """
        self._admins: list[int] = admins
        self._is_admin: bool = is_admin
    async def __call__(self, message: Message) -> bool:
        """
        Проверяет, является ли пользователь администратором.

        :param message: сообщение, которое было отправлено пользователем
        :type message: Message
        :param is_admin: является ли пользователь администратором?
        :type is_admin: bool
        :return: True, если пользователь является администратором, False - если нет
        :rtype: bool
        """
        if self._admins is None:
            _admins = get_id_from_players(PlayerRequest().select_all_admins())
            message.from_user.id in _admins
        found_admin: bool = message.from_user.id in self._admins 
        # Если находит id в списках админов, но притом это роль доолжна быть игроков, то делает 
        return found_admin if self._is_admin else not found_admin
            
    