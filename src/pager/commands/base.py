from abc import abstractmethod
from aiogram import types
class BaseHandler:   
    @abstractmethod
    def check_command(self, message: types.Message):
        pass
            
            
    

