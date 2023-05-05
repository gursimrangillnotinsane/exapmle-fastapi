from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import psycopg2.extras 
from psycopg2.extras  import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine= create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

def get_db(): # TO GET CONNECTION TO DATABASE
   db= sessionlocal()
   try:
      yield db
   finally:
      db.close()

#USE TO CONNECT TO DATABSE DIRECTLY WITHOUT ORM 
####USES PYHTON SQL
# while True:
   
#  try: #connect to a database
#    conn= psycopg2.connect(host="localhost",database="fastapidatabse",user="postgres",password="password",cursor_factory= RealDictCursor )
#    cursor=conn.cursor()
#    print('databse connecton was succesfull')
#    break

#  except Exception as error:
#    print("connection to database was failed")
#    print("Error was",error)
#    time.sleep(2)# waits 2 sec before trying again
