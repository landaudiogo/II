from sqlalchemy.orm import relationship

from ..config import Base
from ..general import DatabaseHandler

class Order(Base, DatabaseHandler):

    __tablename__ = 'order'
    __table_args__ = {'schema': 'planner', 'autoload': True}

    def __init__(self, **kwargs):
        pass


