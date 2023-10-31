import jwt
import datetime
import bcrypt

import user_funcs


def login(email ,password, organization):
    # check if the user exists
    try:
        user = user_funcs.get_user_by_email(email, organization)
        if user:
            # check if the password is correct
            pwd = password.encode('utf-8')
            if bcrypt.checkpw(pwd, user.hash.encode('utf-8')):
                # create a jwt token
                jwt_encoded = createJWT(user)
                return jwt_encoded
            else:
                return "Incorrect Password"
        else:
            return "User does not exist"
    except Exception as e:
        return f"Error: {e}"

def createJWT(user):
    payload = {
        "id": user.id,
        "organization": user.organization,
        "roles": user.roles,
        "first_name": user.first_name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    jwt_encoded = jwt.encode( payload, 'secret', algorithm='HS256')
    res = {
        'token': jwt_encoded,
        'id': user.id,
    }
    return res

def decodeJWT(jwt_encoded):
    try:
        ans = jwt.decode(jwt_encoded, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        ans = "Invalid"
    except jwt.InvalidTokenError:
        ans = "Invalid"
    return ans

def check_superadmin_JWT(jwt_encoded):
    try:
        res = decodeJWT(jwt_encoded)
        if res["roles"] == "superadmin":
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    
def check_admin_JWT(jwt_encoded):
    try:
        res = decodeJWT(jwt_encoded)
        if res["roles"] == "superadmin" or res["roles"] == "admin":
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    
def getOTP(email, id, company):
    user = user_funcs.get_user_by_id(id, company)
    if user:
        otp = user_funcs.createOTP()
        res = user_funcs.update_pass(id, company, otp)
        otp_res = user_funcs.send_OTP(email, otp, 'Password Change Request')
        if otp_res.startswith("Error"):
            return otp_res
        return res
    else:
        return "Invalid ID"

