from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, 
    ForeignKey, 
    Integer
)

from ..config import Base
from ..general.mixins import MixinsDatabase, MixinsClass

class Unload(Base, MixinsDatabase, MixinsClass):

    __tablename__ = 'unload'
    __table_args__ = {'schema': 'mes', 'autoload': True}

    order_number = Column(Integer, ForeignKey('mes.order.order_number'))
    order_number._relationship = 'order'

    order = relationship('Order', back_populates='unloads')

    cls_metadata_set        = False
    cls_relationships_data  = False

    def __init__(self, **kwargs):
        if not self.cls_metadata_set: 
            Unload._class_init()
        elif not self.cls_relationships_data:
            Unload._class_init()
        else: 
            MixinsClass.__init__(self, **kwargs)
