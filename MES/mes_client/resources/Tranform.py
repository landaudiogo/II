from ..config import Base
from ..general import DatabaseHandler

class Transform(Base, DatabaseHandler):
    __tablename__ = 'transform'
    __table_args__ = {'schema': 'mes', 'autoload': True}

    def __init__(self):
        pass
