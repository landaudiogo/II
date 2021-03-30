from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from .config import engine

Session = sessionmaker(bind=engine)

from .resources import (
    Order,
    Machine, 
    Piece, 
    Transform, 
    Unload, 
    MesSession
)

models = [
    Order,
    Machine,
    Piece, 
    Transform, 
    Unload, 
    MesSession
]

[model() for i in range(2) for model in models]

@contextmanager
def session_manager():
    session = Session()
    try:
        yield session
    except Exception as e:
        raise e
    finally:
        session.close()

