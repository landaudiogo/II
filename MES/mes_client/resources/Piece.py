from ..config import Base
from ..general import DatabaseHandler

class Piece(Base, DatabaseHandler):
    __tablename__ = 'piece'
    __table_args__ = {'schema': 'mes', 'autoload': True}

    def __init__(self):
        pass
