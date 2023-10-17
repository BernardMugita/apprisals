import bcrypt
import os
import smtplib
import random as r
import math as m
from email.mime.text import MIMEText

import models
from auth import createJWT



def get_users(organization):
    usr_table = models.create_users_table(organization)
    users = models.session.query(usr_table).all()
    return users

def get_user_by_email(email, organization):
    usr_table = models.create_users_table(organization)
    if email:
        user = models.session.query(usr_table).filter_by(email=email).first()
    else:
        user = None
    return user

def get_user_by_id(id, organization):
    usr_table = models.create_users_table(organization)
    if id:
        user = models.session.query(usr_table).filter_by(id=id).first()
    else:
        user = None
    return user



def send_OTP(email, otp):
    try:
        # create message object instance
        msg = MIMEText(f"Your One Time Password is {otp}")
        msg['Subject'] = "Your account was created successfully"
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
        new_user = usr_table(username=username, roles=roles, first_name=first_name, last_name=last_name, email=email, organization=organization, telephone=telephone, hash=hash, job_role=job_role)
        models.session.add(new_user)
        models.session.commit()
        usr_obj = models.session.query(usr_table).filter_by(email=email).filter_by(first_name=first_name).first()
        res = {
            "id": usr_obj.id,
            "username": usr_obj.username,
            "roles": usr_obj.roles,
            "first_name": usr_obj.first_name,
            "last_name": usr_obj.last_name,
            "email": usr_obj.email,
            "organization": usr_obj.organization,
            "telephone": usr_obj.telephone,
            "job_role": usr_obj.job_role,
            "OTP": otp,
            "has_changed_pass": usr_obj.has_changed_pass
        }
        return res
    except Exception as e:
        print(e)
        return f"Error: {e}"

# print(create_user("marto", "superadmin", "martin", "briston", "martinbriston01@gmail.com", "bazu", "865987452", "Backend Engineer"))


def update_pass(userid, company, newpass): # for first time change
    try:
        usr_table = models.create_users_table(company)
        user = models.session.query(usr_table).filter_by(id=userid).first()
        hash = bcrypt.hashpw(newpass.encode('utf-8'), bcrypt.gensalt())
        # if user.has_changed_pass == True:
        #     return "User has already changed password"
        user.hash = hash
        user.has_changed_pass = False
        models.session.commit()
        token = createJWT(user)
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
        usr_table = models.create_users_table(company)
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

