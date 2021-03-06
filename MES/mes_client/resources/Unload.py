from ..config import Base
from ..general import DatabaseHandler

class Unload(Base, DatabaseHandler):
    __tablename__ = 'unload'
    __table_args__ = {'schema': 'mes', 'autoload': True}

    def __init__(self):
        pass
