
from pager.databases.models import Player
from pager.databases.requests.game import GameRequest


async def get_id_from_players(players: Player) -> list[int]:
    return [player.id_tg for player in players]


async def get_name_all_players_from_group(number_group: int) -> str:
    message_str = ""
    players = await GameRequest.get_players_from_game(number_group)
    for player in players:
        message_str += f"{player.player_name}\n"
    return message_str
    