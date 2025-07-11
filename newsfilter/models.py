from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base=declarative_base()


class Utilisateur(Base):
    __tablename__='utilisateurs'

    id=Column(Integer,primary_key=True,index=True)
    email=Column(String(50),unique=True,index=True)
    username=Column(String(50))