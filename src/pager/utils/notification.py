import datetime
from pager.databases.requests.game import GameRequest
from pager.databases.requests.player import PlayerRequest
from pager.utils.bot import BotManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Notification:
    @staticmethod
    async def notification_group(number_group: int, message_str: str, new_data = ""):
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
                
    @staticmethod 
    async def notification_group_date(number_group: int, date: str):
        number_group = 1
        datatime = datetime.datetime.strptime(date, '%d.%m.%Y')
        datatime -= datetime.timedelta(days=1)
        datatime = datatime.replace(hour=15, minute=0, second=0)
        scheduler = AsyncIOScheduler()
        scheduler.add_job(Notification.notification_group, "date", run_date=datatime, timezone="Europe/Moscow", args=[number_group, "Тест уведомления игры, игра будет", date])
        scheduler.start()