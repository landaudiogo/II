from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, 
    ForeignKey, 
    Integer
)

from ..config import Base
from ..general.mixins import MixinsDatabase, MixinsClass

class Transform(Base, MixinsDatabase, MixinsClass):

    __tablename__ = 'transform'
    __table_args__ = {'schema': 'mes', 'autoload': True}
    
    order_number = Column(Integer, ForeignKey('mes.order.order_number'))
    order_number._relationship = 'order'

    order = relationship('Order', back_populates='transformations')
    pieces = relationship('Piece', back_populates='transform')

    cls_metadata_set        = False
    cls_relationships_data  = False

    def __init__(self, **kwargs):
        if not self.cls_metadata_set: 
            Transform._class_init()
        elif not self.cls_relationships_data:
            Transform._class_init()
        else: 
            MixinsClass.__init__(self, **kwargs)
