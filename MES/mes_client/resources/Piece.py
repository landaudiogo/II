from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, 
    ForeignKey, 
    Integer
)

from ..config import Base
from ..general.mixins import (
    MixinsClass, 
    MixinsDatabase
)

class Piece(Base, MixinsClass, MixinsDatabase):

    __tablename__ = 'piece'
    __table_args__ = {'schema': 'mes', 'autoload': True}

    transform_id = Column(Integer, ForeignKey('mes.transform.transform_id'))
    transform_id._relationship = 'transform'

    transform = relationship('Transform', back_populates='pieces')

    cls_metadata_set        = False
    cls_relationships_data  = False

    def __init__(self, **kwargs):
        if not self.cls_metadata_set:
            Piece._class_init()
        elif not self.cls_relationships_data:
            Piece._class_init()
        else: 
            MixinsClass.__init__(self, **kwargs)
