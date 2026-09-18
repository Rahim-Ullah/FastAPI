from sqlalchemy import create_engine, Column, Integer, String
from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# DATABASE_URL = "sqlite:///./test.db"  
# engine = create_engine('DATABASE_URL', echo=True, connect_args={"check_same_thread": False}) 

app = FastAPI()

# The same job is done above in two lines, but this way is more readable
engine = create_engine('sqlite:///test.db', echo=True, connect_args={"check_same_thread": False}) # echo=True for debugging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # autoflush=False for debugging, it is not needed in production, it means that the session will not automatically flush changes to the database before queries are executed, which can be useful for debugging but may lead to unexpected behavior in production.

Base = declarative_base() # Base is a class that represents the database table structure
# Base.metadata(engine) can be created above the model classes, but it is better to create it after the model classes are defined, so that the table structure is created based on the model classes.

db = SessionLocal() # db is a session object that represents a database connection

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    # def __repr__(self):
    #     return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

Base.metadata.create_all(engine) # create_all() is a method of the Base class that creates the database table structure based on the model classes defined in the declarative base


def get_db():
    db = SessionLocal() # create a new session object
    try:
        yield db # yield the session object to the caller
    finally:
        db.close() # close the session object
        
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"Connection": "DB connected"}