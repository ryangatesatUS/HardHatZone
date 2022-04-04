from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from os import environ, path

print("Starting our script")

engine = create_engine('mssql+pyodbc:///?odbc_connect=Driver={FreeTDS};TDS_Version=7.4;Port=1433;Database=AvailabilityManagement_Beta; Server=D40DUSGRS01.DEV.US.CORP; UID=svc.api; PWD=thi5isThepa$$word;')

print("Ending our script")