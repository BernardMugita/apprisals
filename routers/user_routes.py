from fastapi import APIRouter
from fastapi import Request
import json
import user_funcs
import redis_funcs

router = APIRouter()


@router.post("/users/getall")
async def getallusers(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == "Invalid":
            return "Invalid Token"
        else:
            if redis_funcs.redis_exists(f"{usr['organization']}", 'allusers'):
                res = redis_funcs.redis_get(f"{usr['organization']}", 'allusers')
                return json.loads(res)
            else:
                users = user_funcs.get_users(usr["organization"])
                redis_funcs.redis_set(f"{usr['organization']}", 'allusers' ,json.dumps(users))
                return users
    else:
        return "Invalid Token" 
    
@router.post("/users/getbyid")
async def getuserbyid(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == "Invalid":
            return "Invalid Token"
        else:
            # data = await request.json()
            # id = data["id"] # provide ID of user to get
            users = user_funcs.get_user_by_id(usr['id'], usr["organization"]) 
            return users
    else:
        return "Invalid Token" 

@router.post("/users/login")
async def login(request: Request):
    data = await request.json()
    email = data["email"]
    password = data["password"]
    company = data["company"]
    # if redis_funcs.redis_exists(f"{company}", 'auth'):
    #     res = redis_funcs.redis_get(f"{company}", 'auth')
    #     return json.loads(res)
    # else:
    ans = user_funcs.auth.login(email, password, company)
    # redis_funcs.redis_set(f"{company}", 'auth', json.dumps(ans))
    return ans


@router.post("/users/createuser")
async def createuser(request: Request):
    data = await request.json()
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.check_admin_JWT(auth_token)
        if usr == False:
            return "Invalid Token"
        else:
            username = data["username"]
            roles = data["roles"]
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email"]
            organization = data["organization"]
            telephone = data["telephone"]
            job_role = data["job_role"]
            ans = user_funcs.create_user(username, roles, first_name, last_name, email, organization, telephone, job_role)
            redis_funcs.redis_del(f"{organization}", 'allusers')
            return ans
    else:
        return "Invalid Token"
    
    
@router.post("/users/updateuser")
async def updateuser(request: Request):
    data = await request.json()
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.check_admin_JWT(auth_token)
        if usr == False:
            return "Invalid Token"
        else:
            id = data["id"]
            username = data["username"]
            roles = data["roles"]
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email"]
            organization = data["organization"]
            telephone = data["telephone"]
            job_role = data["job_role"]
            cmpid = data["cmpid"] # TODO: check if this is needed
            ans = user_funcs.edit_user(id, username, roles, first_name, last_name, email, organization, telephone, job_role, cmpid)
            return ans
    else:
        return "Invalid Token"
    
@router.post("/users/firsttimechange")
async def firsttimechange(request: Request):
    data = await request.json()
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            id = usr['id']
            res = user_funcs.update_pass(id, usr['organization'], data["password"])
            return res
    else:
        return "Invalid Token"
    
@router.post("/users/getotp")
async def getotp(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            id = usr['id']
            userobj = user_funcs.get_user_by_id(id, usr['organization'])
            print(userobj)
            res = user_funcs.auth.getOTP(userobj.email, id, usr['organization'])
            return res
    else:
        return "Invalid Token"
    
@router.post("/users/changepass")
async def changepass(request: Request):
    data = await request.json()
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = user_funcs.auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            id = usr['id']
            res = user_funcs.change_pass(data["otp"], id, usr['organization'], data["password"])
            return res
    else:
        return "Invalid Token"
