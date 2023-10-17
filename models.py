from sqlalchemy import create_engine, Column, String, Integer, Enum, ForeignKey, Float, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PydanticEnum
from pydantic import BaseModel
from dotenv import load_dotenv
import pymysql
import bcrypt
import smtplib
from email.mime.text import MIMEText

import uuid
import os


Base = declarative_base()  # Create a declarative base class for SQLAlchemy

# load dotenv
load_dotenv()

# Get the database credentials from environment variables
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

database_uri = f"mysql+pymysql://root:{password}@localhost/{database}"


def mysqlconnect():

    conn = pymysql.connect(

        # database credentials
        host='localhost',
        user='root',
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
    superadmin = "superadmin"
    superuser = "superuser"


class PayslipStatus(str, Enum):  # Enum class for payslip status
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class TaskStatus(str, Enum):  # Enum class for task status
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"


def create_users_table(company_name):
        Base.metadata.clear()
        class User(Base):
            __tablename__ = f"{company_name}_users"

            id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
            username = Column(String(50), nullable=False)
            roles = Column(String(50), nullable=False)
            first_name = Column(String(50), nullable=False)
            last_name = Column(String(50), nullable=False)
            email = Column(String(100), nullable=False, unique=True)
            organization = Column(String(100), nullable=False)
            telephone = Column(String(20), nullable=False)
            hash = Column(String(255), nullable=False)
            job_role = Column(String(255), nullable=False)
            has_changed_pass = Column(Boolean, nullable=False, default=False)
        return User

def create_tasks_table(company_name):
    # Pydantic model for the employee table
    Base.metadata.clear()
    class Tasks(Base):
        __tablename__ = f"{company_name}_tasks"

        id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
        title = Column(String(255), nullable=False)
        description = Column(String(1000), nullable=False)
        status = Column(String(50), nullable=False)
        assigned_to = Column(String(255), nullable=False) # change to foreign key??
        task_type = Column(String(50), nullable=False)
        rating = Column(Integer, nullable=False)
        feedback = Column(String(1000), nullable=False)
    return Tasks
    
def create_payslips_table(company_name):
    Base.metadata.clear()
    class Payslips(Base):
        __tablename__ = f"{company_name}_payslips"

        id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
        employee_id = Column(String(255), nullable=False) # change to foreign key??
        employee_name = Column(String(255), nullable=False)
        prepared_by = Column(String(255), nullable=False)
        date = Column(String(20), nullable=False)
        period = Column(String(20), nullable=False)
        amount = Column(Float, nullable=False)
        status = Column(String(50), nullable=False)
    return Payslips

def create_messages_table(company_name):
    Base.metadata.clear()
    class Messages(Base):
        __tablename__ = f"{company_name}_messages"

        id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
        sender = Column(String(255), nullable=False)
        receiver = Column(String(255), nullable=False)
        date = Column(String(20), nullable=False)
        message = Column(String(1000), nullable=False)
    return Messages

Session = sessionmaker(bind=engine)  # Create a session
session = Session()


# Create tables in the database
def create_tables():
    Base.metadata.create_all(engine)

def create_company_tables(company_name):
    try:
        usr_table = f"{company_name}_users"
        tasks_table = f"{company_name}_tasks"
        payslips_table = f"{company_name}_payslips"
        messages_table = f"{company_name}_messages"
        
        usr_table = create_users_table(company_name)
        tasks_table = create_tasks_table(company_name)
        payslips_table = create_payslips_table(company_name)
        messages_table = create_messages_table(company_name)

        Base.metadata.create_all(engine)
        return "Success"
    except Exception as e:
        return f"Error: {e}"

def delete_company_tables(company_name):
    try:
        usr_table = f"{company_name}_users"
        tasks_table = f"{company_name}_tasks"
        payslips_table = f"{company_name}_payslips"
        messages_table = f"{company_name}_messages"

        usr_table = create_users_table(company_name)
        tasks_table = create_tasks_table(company_name)
        payslips_table = create_payslips_table(company_name)
        messages_table = create_messages_table(company_name)

        Base.metadata.drop_all(engine)
        return "Success"
    except Exception as e:
        return f"Error: {e}"
        


# use this to test the create_company_tables function
# create_company_tables("bazu")
# delete_company_tables("bazu")




