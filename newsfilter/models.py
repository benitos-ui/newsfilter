from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash

Base=declarative_base()


class Utilisateur(Base):
    __tablename__='utilisateurs'

    id=Column(Integer,primary_key=True,index=True)
    email=Column(String(50),unique=True,index=True)
    pays=Column(String(50))
    ville=Column(String)
    age=Column(Integer,nullable=False)
    nom=Column(String(50))
    prenom=Column(String(50))
    user=relationship("User",back_populates='utilisateur')


class  User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True,index=True)
    password_hash=Column(String(128)) 
    username=Column(String(50))
    user_id=Column(Integer,ForeignKey('utilisateurs.id')) 
    utilisateur=relationship('Utilisateur',back_populates="user")   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)