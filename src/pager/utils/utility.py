
from pager.databases.models import Player


async def get_id_from_players(players: Player) -> list[int]:
    return [player.id_tg for player in players]


