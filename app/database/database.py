from app.database.base import Base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.models.user_model import User
import logging
logging.basicConfig(level=logging.DEBUG)


DATABASE_URL = "mysql+mysqlconnector://uadmin:123456@localhost:3306/becho_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create tables


def init_db():
    logging.debug('Connecting to database...')
    session = SessionLocal()
    Base.metadata.create_all(bind=engine)
    logging.debug('Creating tables...')

    session.commit()
    session.close()
    logging.debug('Tables created successfully.')

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables created successfully.", tables)


# Dependency for getting the database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
