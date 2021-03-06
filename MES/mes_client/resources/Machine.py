from ..config import Base
from ..general import DatabaseHandler

class Machine(Base, DatabaseHandler):
    __tablename__ = 'machine'
    __table_args__ = {'schema': 'mes', 'autoload': True}

    def __init__(self):
        pass
