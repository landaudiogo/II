from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Metadata

engine = create_engine('postgresql://postgres:postgres@postgres:5432/ii')
Base = declarative_base()
Base.metadata.bind = engine
