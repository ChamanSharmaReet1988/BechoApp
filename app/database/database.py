from app.database.base import Base
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from app.models.user_model import User
import logging
logging.basicConfig(level=logging.DEBUG)


DATABASE_URL = "mysql+mysqlconnector://uadmin:123456@localhost:3306/becho_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    logging.debug('Connecting to database...')
    session = SessionLocal()
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        logging.debug('Creating tables...')
    except Exception as e:
        print(f"Error creating tables: {e}")

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


# Example: Add a new column
# query = "ALTER TABLE users ADD COLUMN profileImage VARCHAR(512)"
# query = "ALTER TABLE users DROP COLUMN profileImage"
# with engine.connect() as connection:
#     connection.execute(text(query))
