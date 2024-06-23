from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import CONFIG, DATA_PATH

Base = declarative_base()
DATABASE_URL = CONFIG('DATABASE_URL', default='sqlite:///' + DATA_PATH + 'app.db')
print("db url:" + DATABASE_URL)
ENGINE = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
DB_SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
print("init db done")
