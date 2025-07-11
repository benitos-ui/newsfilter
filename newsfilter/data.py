from sqlalchemy import create_engine
from models import Base
from sqlalchemy.orm import sessionmaker

db_path = 'sqlite:///test_alchemy.db'

engine=create_engine(db_path)

try:
    
    

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Session=sessionmaker(bind=engine)
    session=Session()

    
except Exception as ex:
    print(ex)    