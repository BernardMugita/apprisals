from sqlalchemy import create_engine, Column, String, Integer, Enum, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PydanticEnum
from pydantic import BaseModel
from dotenv import load_dotenv
import pymysql
import bcrypt
import smtplib
from email.mime.text import MIMEText
import re

import uuid
import os


Base = declarative_base()

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


def create_model_tables(company_name):
    # Base = declarative_base()  # Create a declarative base class for SQLAlchemy
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

        company_id = Column(String(36), ForeignKey("companies.id"))
        company = relationship("Company", foreign_keys=[company_id])

    class Company(Base):
        __tablename__ = "companies"

        id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
        name = Column(String(255), nullable=False)
        email = Column(String(255), nullable=False)
        telephone = Column(String(20), nullable=False)
        address = Column(String(255), nullable=False)
        city = Column(String(255), nullable=False)
        country = Column(String(255), nullable=False)
        domain_name = Column(String(255), nullable=False)
        table_name = Column(String(255), nullable=False)
        employees = relationship("User", backref="companies")

    class Tasks(Base):
        __tablename__ = f"{company_name}_tasks"

        id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
        title = Column(String(255), nullable=False)
        description = Column(String(1000), nullable=False)
        status = Column(String(50), nullable=False)
        assigned_to_id = Column(String(255), ForeignKey(f"{company_name}_users.id"))
        assigned_by_id = Column(String(255), ForeignKey(f"{company_name}_users.id"))

        assigned_to = relationship("User", foreign_keys=[assigned_to_id])
        assigned_by = relationship("User", foreign_keys=[assigned_by_id])

        task_type = Column(String(50), nullable=False)
        rating = Column(Integer, nullable=False)
        feedback = Column(String(1000), nullable=False)
        due_date = Column(String(20), nullable=False)

    class Payslips(Base):
        __tablename__ = f"{company_name}_payslips"

        id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
        employee_id = Column(String(255), ForeignKey(f"{company_name}_users.id")) 
        prepared_by_id = Column(String(255), ForeignKey(f"{company_name}_users.id"))

        employee = relationship("User", foreign_keys=[employee_id])
        prepared_by = relationship("User", foreign_keys=[prepared_by_id])

        date = Column(String(20), nullable=False)
        period = Column(String(20), nullable=False)
        amount = Column(Float, nullable=False)
        status = Column(String(50), nullable=False)
        deductions = Column(String(2096), nullable=False)
        additions = Column(String(2096), nullable=False)

    class Messages(Base):
        __tablename__ = f"{company_name}_messages"

        id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
        sender_id = Column(String(255), ForeignKey(f"{company_name}_users.id"))
        receiver_id = Column(String(255), ForeignKey(f"{company_name}_users.id"))

        sender = relationship("User", foreign_keys=[sender_id])
        receiver = relationship("User", foreign_keys=[receiver_id])

        date = Column(String(20), nullable=False)
        message = Column(String(1000), nullable=False)

    return User, Company, Tasks, Payslips, Messages

Session = sessionmaker(bind=engine)  # Create a session
session = Session()


# Create tables in the database
def create_tables():
    Base.metadata.create_all(engine)

def extract_name(domain):
    reg_patt = r"(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)"
    domain_name = re.match(reg_patt, domain).group(1)
    domain_patt = r"([a-zA-Z0-9-]+)(\.[a-zA-Z]{2,5})?(\.[a-zA-Z]+$)"
    final = re.match(domain_patt, domain_name).group(1)
    return final

def create_company(company_name, email, telephone, address, city, country, domain_name):
    try:
        table_name = extract_name(domain_name)
        User, Company, Tasks, Payslips, Messages = create_model_tables(table_name)
        # Base.metadata.create_all(engine)
        # res = create_company_tables(table_name)
        # if res != "Success":
        #     return f"Error: {res}"
        # else:
            # Base.metadata.clear()
            # companies_table = create_companies_table(user)
        new_company = Company(name=company_name, email=email, telephone=telephone, address=address, city=city, country=country, domain_name=domain_name, table_name=table_name)
        session.add(new_company)
        session.commit()
        return "Success"    
    except Exception as e:
        return f"Error: {e}"

def create_company_tables(company_name):
    try:
        usr_table = f"{company_name}_users"
        tasks_table = f"{company_name}_tasks"
        payslips_table = f"{company_name}_payslips"
        messages_table = f"{company_name}_messages"
        
        User, Company, Tasks, Payslips, Messages = create_model_tables(company_name)
        Base.metadata.create_all(engine)
        return "Success"
    except Exception as e:
        return f"Error: {e}"

# print(create_company_tables("bazu"))

def delete_company_tables(company_name):
    try:
        usr_table = f"{company_name}_users"
        tasks_table = f"{company_name}_tasks"
        payslips_table = f"{company_name}_payslips"
        messages_table = f"{company_name}_messages"

        User, Company, Tasks, Payslips, Messages = create_model_tables(company_name)
        Base.metadata.drop_all(engine, tables=[User.__table__, Tasks.__table__, Payslips.__table__, Messages.__table__])
        return "Success"
    except Exception as e:
        return f"Error: {e}"
        


# use this to test the create_company_tables function
# create_company_tables("bazu")
# print(delete_company_tables("bolt"))




