import bcrypt
import os
import smtplib
import random as r
import math as m
from email.mime.text import MIMEText

import models
import auth


def user_parser(user, many=False):
    if many:
        return [user_parser(item) for item in user]
    else:
        return {
            "id": user.id,
            "username": user.username,
            "roles": user.roles,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "organization": user.organization,
            "telephone": user.telephone,
            "job_role": user.job_role,
            "has_changed_pass": user.has_changed_pass,
            "company_info": {
                "id": user.company.id,
                "name": user.company.name,
                "email": user.company.email,
                "telephone": user.company.telephone,
                "address": user.company.address,
                "city": user.company.city,
                "country": user.company.country,
                "domain_name": user.company.domain_name,
                "table_name": user.company.table_name,
            }
        }

def get_users(organization):
    models.Base.metadata.clear()
    usr_table = models.create_users_table(organization)
    company = models.create_companies_table(usr_table)
    users = models.session.query(usr_table).all()
    users = user_parser(users, many=True)
    return users

def get_user_by_email(email, organization):
    models.Base.metadata.clear()
    usr_table = models.create_users_table(organization)
    company = models.create_companies_table(usr_table)
    if email:
        user = models.session.query(usr_table).filter_by(email=email).first()
        # user = user_parser(user)
    else:
        user = None
    return user

def get_user_by_id(id, organization):
    models.Base.metadata.clear()
    usr_table = models.create_users_table(organization)
    company = models.create_companies_table(usr_table)
    if id:
        user = models.session.query(usr_table).filter_by(id=id).first()
        obj = user_parser(user)
    else:
        user = None
    return obj

    

def send_OTP(email, otp, subject="Your account was created successfully"):
    try:
        # create message object instance
        msg = MIMEText(f"Your One Time Password is {otp}")
        msg['Subject'] = subject
        msg['From'] = 'noreply@finalyze.app'
        msg['To'] = email

        s = smtplib.SMTP_SSL(f"{os.getenv('EMAIL_HOST')}:{os.getenv('EMAIL_PORT')}")
        s.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        s.send_message(msg)
        s.quit()
        return "Success"
    except Exception as e:
        print(e)
        return f"Error: {e}"

def createOTP(): 
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = "" 
    varlen= len(string) 
    for i in range(6) : 
        OTP += string[m.floor(r.random() * varlen)] 
    return (OTP) 

# for creating a user
def create_user(username, roles, first_name, last_name, email, organization, telephone, job_role):
    usr_table = models.create_users_table(organization) # assuming the organization is the company name
    # generate a one time password
    otp = createOTP()
    otp_res = send_OTP(email, otp)
    if otp_res.startswith("Error"):
        return otp_res
    hash = bcrypt.hashpw(otp.encode('utf-8'), bcrypt.gensalt())
    try:
        # models.Base.metadata.clear()   
        compnytable = models.create_companies_table(usr_table)
        company = models.session.query(compnytable).filter_by(name="bazu").first() #TODO: change this to the company name
        new_user = usr_table(username=username, roles=roles, first_name=first_name, last_name=last_name, email=email, organization=organization, telephone=telephone, hash=hash, job_role=job_role, company_id=company.id)
        models.session.add(new_user)
        models.session.commit()
        usr_obj = models.session.query(usr_table).filter_by(email=email).filter_by(first_name=first_name).first()
        res = user_parser(usr_obj)
        return res
    except Exception as e:
        print(e)
        return f"Error: {e}"

# models.Base.metadata.clear()
# print(create_user("marto", "superadmin", "martin", "briston", "martinbriston01@gmail.com", "bazu", "865987452", "Backend Engineer", company))

def edit_user(id, username, roles, first_name, last_name, email, organization, telephone, job_role, company):
    try:
        models.Base.metadata.clear()
        usr_table = models.create_users_table(organization)
        company_table = models.create_companies_table(usr_table)
        user = models.session.query(usr_table).filter_by(id=id).first()
        user.username = username
        user.roles = roles
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.organization = organization
        user.telephone = telephone
        user.job_role = job_role
        user.company_id = company
        models.session.commit()
        return "Success"
    except Exception as e:
        print(e)
        return f"Error: {e}"

def update_pass(userid, company, newpass): # for first time change
    try:
        models.Base.metadata.clear()
        usr_table = models.create_users_table(company)
        company_table = models.create_companies_table(usr_table)
        user = models.session.query(usr_table).filter_by(id=userid).first()
        hash = bcrypt.hashpw(newpass.encode('utf-8'), bcrypt.gensalt())
        # if user.has_changed_pass == False:
        #     return "User has already changed password"
        user.hash = hash
        user.has_changed_pass = False
        models.session.commit()
        token = auth.createJWT(user)
        return {
            'success': True,
            'token': token,
        }
    except Exception as e:
        print(e)
        return {
            'success': False,
            'error': e
        }
    
def change_pass(otp, id, company, newpass):
    try:
        models.Base.metadata.clear()
        usr_table = models.create_users_table(company)
        company_table = models.create_companies_table(usr_table)
        user = models.session.query(usr_table).filter_by(id=id).first()
        if user.has_changed_pass == True:
            return "User has already changed password"
        if bcrypt.checkpw(otp.encode('utf-8'), user.hash.encode('utf-8')):
            hash = bcrypt.hashpw(newpass.encode('utf-8'), bcrypt.gensalt())
            user.hash = hash
            user.has_changed_pass = True
            models.session.commit()
            return "Success"
        else:
            return "Invalid OTP"
    except Exception as e:
        print(e)
        return f"Error: {e}"

