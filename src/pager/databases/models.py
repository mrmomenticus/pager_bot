from sqlalchemy import (
    ARRAY,
    Column,
    ForeignKey,
    String,
    Integer,
    Boolean,
    Date,

)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, MappedColumn, relationship

class BaseModel(DeclarativeBase):
    pass


class Player(BaseModel):
    __tablename__ = "Players"
    id_tg: Mapped[int] = MappedColumn(primary_key=True)
    inventory: Mapped["Inventory"] = relationship(back_populates="player")
    game_id: Mapped[int] = MappedColumn(ForeignKey("Game.number_group"))
    username: Mapped[str] = MappedColumn(String(255))
    player_name: Mapped[str] = MappedColumn(String(255))
    is_admin: Mapped[bool] = MappedColumn(Boolean(), default=False)
    photo_state = Column(ARRAY(String), nullable=True)

    game: Mapped["Game"] = relationship(
        back_populates="players"
    )  # Это свойство должно быть здесь

    def clear(self):
        self.id_tg = None
        self.username = None
        self.player_name = None
        self.game_id = None
        self.is_admin = None


class Game(BaseModel):
    __tablename__ = "Game"
    number_group: Mapped[int] = MappedColumn(primary_key=True)
    game_name: Mapped[str] = MappedColumn(String(255))
    date = MappedColumn(Date())

    players: Mapped[list["Player"]] = relationship("Player", back_populates="game")
    npcs: Mapped[list["Npc"]] = relationship(back_populates="game")
    help_game: Mapped["HelpGame"] = relationship(back_populates="game")
    mission: Mapped[list["Mission"]] = relationship(back_populates="game")

    def __str__(self):
        return f"{self.date}"


class Inventory(BaseModel):
    __tablename__ = "Inventory"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = MappedColumn(Integer, ForeignKey("Players.id_tg"))
    money: Mapped[int] = MappedColumn(Integer)

    player: Mapped["Player"] = relationship(back_populates="inventory")
    stuff: Mapped[list["Stuff"]] = relationship(back_populates="inventory")


class Stuff(BaseModel):
    __tablename__ = "Stuff"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)
    invetory_id: Mapped[int] = MappedColumn(Integer, ForeignKey("Inventory.id"))
    title: Mapped[str] = MappedColumn(String(255))
    price: Mapped[int] = MappedColumn(Integer)
    description: Mapped[str] = MappedColumn(String(255))

    inventory: Mapped["Inventory"] = relationship(back_populates="stuff")

class Npc(BaseModel):
    __tablename__ = "Npc"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = MappedColumn(Integer, ForeignKey("Game.number_group"))
    name: Mapped[str] = MappedColumn(String(128))
    local: Mapped[str] = MappedColumn(String(255))
    description: Mapped[str] = MappedColumn(String(1024))
    
    game: Mapped["Game"] = relationship(back_populates="npcs")
    
    
class HelpGame(BaseModel):
    __tablename__ = "HelpGame"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = MappedColumn(Integer, ForeignKey("Game.number_group"))
    path: Mapped[str] = MappedColumn(String(512))
    
    game: Mapped["Game"] = relationship(back_populates="help_game")
    
    
class Mission(BaseModel):
    __tablename__ = "Mission"
    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = MappedColumn(Integer, ForeignKey("Game.number_group"))
    local: Mapped[str] = MappedColumn(String(255))
    desctription: Mapped[str] = MappedColumn(String(6000))
    reward: Mapped[str] = MappedColumn(String(255))
    
    game: Mapped["Game"] = relationship(back_populates="mission")
    