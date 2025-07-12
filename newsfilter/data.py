from sqlalchemy import create_engine
from models import Base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

db_path = 'sqlite:///test_alchemy.db'
load_dotenv()
engine=create_engine(db_path)

try:
    
    

   # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    print("success")
    print("USERNAME:", os.getenv("MAIL_USERNAME"))
    print("SENDER:", os.getenv("MAIL_DEFAULT_SENDER"))


    
except Exception as ex:
    print(ex)    