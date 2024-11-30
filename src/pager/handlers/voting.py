import logging
from aiogram import F, Router, types
from pager import keyboards
from pager.databases.requests.player import PlayerRequest
from pager.filter import Role
from pager.handlers.base import BaseHandler
from pager.utils.bot import BotManager
from pager.databases.requests.game import GameRequest

#TODO: Это костыль класс, надо изменять
class Voting(BaseHandler):
    voiting_router = Router()
    voiting_router.message.filter(Role(is_admin=False))

    
    @staticmethod
    async def send_quick_poll(chat_id: int, question: str):
        bot = BotManager().get_pager_bot().get_raw_bot()
        players = await GameRequest.get_players_from_game(number_group=chat_id)
        for player in players:
            try:
                if player.id_tg != 150536965:
                    await bot.send_message(chat_id=player.id_tg, text=question, protect_content=True, reply_markup=keyboards.QuickVote().get_keyboard())
            except Exception as e:
                logging.error(f"Ошибка при отправке вопроса игроку {player.id_tg}: {str(e)}")
        logging.info(f"Вопрос '{question}' успешно отправлен всем игрокам.")
    
    @voiting_router.message(F.text.in_(['Да', 'Нет']))
    async def cmd_answer(message: types.Message):
        player = await PlayerRequest.select_player(message.from_user.id)
        bot = BotManager().get_pager_bot().get_raw_bot()
        await message.answer("Ответ получен", reply_markup=keyboards.PlayerMenuButtons().get_keyboard())
        await bot.send_message(chat_id=150536965, text=f"Игрок {player.player_name} ответил на вопрос: {message.text}")
        
        
