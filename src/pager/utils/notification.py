from pager.databases.requests.game import GameRequest
from pager.databases.requests.player import PlayerRequest
from pager.utils.bot import BotManager

class Notification:
    @staticmethod
    async def notification_group(number_group: int, message_str: str, new_data):
        bot_manager = BotManager()
        players = await GameRequest.get_players_from_game(number_group)
        for player in players:
            await (
                bot_manager.get_pager_bot()
                .get_raw_bot()
                .send_message(player.id_tg, f"{message_str}: {new_data}")
            )
            
    @staticmethod
    async def notification_player(player_data: int|str, message_str: str, new_data = ""):
        bot_manager = BotManager()
        if isinstance(player_data, int):
            player_id = player_data
        else:
            player = await PlayerRequest.select_player(player_data)
            player_id = player.id_tg
        await (
            bot_manager.get_pager_bot()
            .get_raw_bot()
            .send_message(player_id, f"{message_str} {new_data}")
        )
    
    @staticmethod
    async def notification_all_players(message_str: str, new_data = ""):
        bot_manager = BotManager()
        players = await PlayerRequest.select_all_players()
        for player in players:
            await (
                bot_manager.get_pager_bot()
                .get_raw_bot()
                .send_message(player.id_tg, f"{message_str} {new_data}")
            )
    @staticmethod
    async def notification_admin_game(number_group: int, message_str: str, new_data = ""):
        bot_manager = BotManager()
        players = await GameRequest.get_players_from_game(number_group)
        for player in players:
            if player.is_admin:
                await (
                    bot_manager.get_pager_bot()
                    .get_raw_bot()
                    .send_message(player.id_tg, f"{message_str} {new_data}")
                )