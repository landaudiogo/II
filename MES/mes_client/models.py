from sqlalchemy.orm import sessionmaker

from .config import engine

Session = sessionmaker(bind=engine)

from .resources import (
    Order,
    Machine, 
    Piece, 
    Transform, 
    Unload
)

models = [
    Order,
    Machine,
    Piece, 
    Transform, 
    Unload
]

[model() for i in range(2) for model in models]

