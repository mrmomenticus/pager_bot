
from tracemalloc import BaseFilter
from aiogram.types import Message

from pager.databases.requests.player import PlayerOrm
from pager.utils.utility import get_id_from_players


class IsAdmin(BaseFilter):
    def __init__(self):
        self._admins: list[int] = None
    async def __call__(self, message: Message) -> bool:
        if self._admins is None:
            _admins = get_id_from_players(PlayerOrm().select_all_admins())
            message.from_user.id in _admins
        return message.from_user.id in self._admins
            
    