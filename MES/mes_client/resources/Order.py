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

class Order(Base, MixinsClass, MixinsDatabase):

    __tablename__ = 'order'
    __table_args__ = {'schema': 'mes', 'autoload': True}

    transformations = relationship('Transform', back_populates='order')
    unloads = relationship('Unload', back_populates='order')

    cls_metadata_set        = False
    cls_relationships_data  = False

    def __init__(self, **kwargs):
        if not self.cls_metadata_set: 
            Order._class_init()
        elif not self.cls_relationships_data:
            Order._class_init()
        else: 
            MixinsClass.__init__(self, **kwargs)


