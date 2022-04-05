from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from os import environ, path

print("Starting our script")

odbc_connection=""
engine = create_engine(odbc_connection)

print("Ending our script")