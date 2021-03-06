# Modules/Library Imports and initialization
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
import os
from .config import settings
# import mysql.connector
# from mysql.connector import Error
# from time import sleep


# Dependency for the SQL Alchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Environment Variables for the MySQL Database
# mysql_user = os.environ.get("MYSQL_USER")
# mysql_pass = os.environ.get("MYSQL_PASS")
# pgsql_user = os.environ.get("PGSQL_USER")
# pgsql_pass = os.environ.get("PGSQL_PASS")

# From ENV File
# pgsql_user = settings.database_username
# pgsql_pass = settings.database_password

# Defining the MySQL URL and connecting the the Database
pgsql_url = f"postgresql+psycopg2://{settings.database_username}" \
            f":%s@{settings.database_hostname}:{settings.database_port}" \
            f"/{settings.database_name}" % quote(settings.database_password)
engine = create_engine(pgsql_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Connecting to the MySQL DB. Might not be needed after using SQL Alchemy
# while True:
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                              database=DATABASE_NAME,
#                                              user=mysql_user,
#                                              password=mysql_pass)
#         if connection.is_connected():
#             db_Info = connection.get_server_info()
#             print("Connected to MySQL Server version ", db_Info)
#             cursor = connection.cursor()
#             cursor.execute("select database();")
#             record = cursor.fetchone()
#             print("You're connected to database: ", record)
#         break
#     except Error as e:
#         print(e)
#         sleep(15)
#         break
