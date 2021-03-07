from ..config import Base
from ..general.mixins import (
    MixinsClass, 
    MixinsDatabase
)

class Machine(Base, MixinsClass, MixinsDatabase):

    __tablename__ = 'machine'
    __table_args__ = {'schema': 'mes', 'autoload': True}

    cls_metadata_set        = False
    cls_relationships_data  = False

    def __init__(self, **kwargs):
        if not self.cls_metadata_set: 
            Machine._class_init()
        elif not self.cls_relationships_data:
            Machine._class_init()
        else: 
            MixinsClass.__init__(self, **kwargs)
