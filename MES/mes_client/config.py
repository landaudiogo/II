from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData

engine = create_engine(
    'postgresql://postgres:postgres@localhost:5432/ii',
    echo=False
)

Base = declarative_base()
Base.metadata.bind = engine
