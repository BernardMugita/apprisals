from sqlalchemy import create_engine, Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PydanticEnum
from pydantic import BaseModel
from dotenv import load_dotenv
import pymysql

import uuid
import os

Base = declarative_base()  # Create a declarative base class for SQLAlchemy

# load dotenv
load_dotenv()

# Get the database credentials from environment variables
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
database = os.environ.get('DATABASE')

database_uri = f"mysql+pymysql://{user}:{password}@localhost/{database}"


def mysqlconnect():
    conn = pymysql.connect(

        # database credentials
        host="localhost",
        user=user,
        password=password,
        database=database,
    )

    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchall()
    print("Database version : %s " % data)

    conn.close()  # close the connection


# Update the database URI to use MySQL with the "apprisals" database
engine = create_engine(database_uri, echo=True)


class Role(str, Enum):  # Enum class for roles
    admin = "admin"
    user = "user"


class PayslipStatus(str, Enum):  # Enum class for payslip status
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class TaskStatus(str, Enum):  # Enum class for task status
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"

# Pydantic model for the user table


class User(BaseModel):
    __tablename__ = 'users'

    id: str = Column(String, primary_key=True, default=str(uuid.uuid4()))
    username: str = Column(String, nullable=False)
    roles: str = Column(Role, nullable=False)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    organization: str = Column(String, nullable=False)
    telephone: str = Column(String, nullable=False)


# Pydantic model for the employee table
class Tasks(BaseModel):
    __tablename__ = 'tasks'

    id: str = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)
    status: str = Column(TaskStatus, nullable=False)
    assigned_to: str = Column(String, nullable=False)
    type: str = Column(String, nullable=False)
    rating: str = Column(Integer, nullable=False)
    feedback: str = Column(String, nullable=False)


# Pydantic model for the employee table
class Payslips(BaseModel):
    __tablename__ = 'payslips'

    id: str = Column(String, primary_key=True, default=str(uuid.uuid4()))
    employee_id: str = Column(String, nullable=False)
    employee_name: str = Column(String, nullable=False)
    prepared_by: str = Column(String, nullable=False)
    date: str = Column(String, nullable=False)
    period: str = Column(String, nullable=False)
    amount: float = Column(Integer, nullable=False)
    status: str = Column(PayslipStatus, nullable=False)


# Pydantic model for the employee table
class Messages(BaseModel):
    __tablename__ = 'messages'

    id: str = Column(String, primary_key=True, default=str(uuid.uuid4()))
    sender: str = Column(String, nullable=False)
    receiver: str = Column(String, nullable=False)
    date: str = Column(String, nullable=False)
    message: str = Column(String, nullable=False)


Session = sessionmaker(bind=engine)  # Create a session
session = Session()


# Create tables in the database
def create_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':  # Run the function to create tables
    mysqlconnect()
    create_tables()
