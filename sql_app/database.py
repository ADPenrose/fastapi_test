# Establishing imports.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Defining the type of DB and locating the file inside the project.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Create the engine for the DB. The argument "connect_args" is only needed for sqlite. By default,
# it will only allow one thread to communicate with it. This is done to prevent accidentally sharing
# the same connection for different requests. However, in FastAPI, using normal functions could result
# in more than one thread interacting with the DB for the same request. Thus, this argument tells SQLite
# to allow this.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
# Each one of the "SessionLocal" instances will be a database session. Currently, this class
# is not a database session yet, but once we instanciate it, that instance will be the actual
# session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will inherit from this class later to create each of the DB ORM models.
Base = declarative_base()
