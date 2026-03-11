from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

SQLalchemy_DB_URL = "sqlite:///./campus.db"

engine = create_engine(SQLalchemy_DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Facility(Base): 
    __tablename__ = "facilities" 

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String, index=True, nullable=False)
    category= Column(String, index=True,nullable=False)
    location= Column(String, index=True,nullable=False)
    operating_hours= Column(String, index=True,nullable=False)
    contact_email= Column(String, index=True,nullable=False)

