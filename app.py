from fastapi import FastAPI, Request
import models
import user_funcs
import auth

app = FastAPI()

# call the create_tables() function
# create_tables() # will be done via api call


@app.get("/")
async def root():
    return ("Hello from Nairobi")

@app.post("/users")
async def getallusers(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.decodeJWT(auth_token)
        if usr == "Invalid":
            return "Invalid Token"
        else:
            users = user_funcs.get_users(usr["organization"])
            return users
    else:
        return "Invalid Token" 
    
@app.post("/getbyid")
async def getuserbyid(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.decodeJWT(auth_token)
        if usr == "Invalid":
            return "Invalid Token"
        else:
            users = user_funcs.get_user_by_id(usr["id"], usr["organization"])
            return users
    else:
        return "Invalid Token" 

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data["email"]
    password = data["password"]
    company = data["company"]
    ans = auth.login(email, password, company)
    return ans


@app.post("/createuser")
async def createuser(request: Request):
    data = await request.json()
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.check_admin_JWT(auth_token)
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
            return ans
    else:
        return "Invalid Token"


@app.post("/createcompany")
async def createcompany(request: Request):
    data = await request.json()
    company = data["company"]
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.check_superadmin_JWT(auth_token)
        if usr == False:
            return "Invalid Token"
        else:
            ans = models.create_company_tables(company)
            return ans
    else:
        return "Invalid Token"
    

@app.post("/firsttimechange")
async def firsttimechange(request: Request):
    data = await request.json()
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            id = usr['id']
            res = user_funcs.update_pass(id, usr['organization'], data["password"])
            return res
    else:
        return "Invalid Token"
    
@app.post("/getotp")
async def getotp(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            id = usr['id']
            userobj = user_funcs.get_user_by_id(id, usr['organization'])
            print(userobj)
            res = auth.getOTP(userobj.email, id, usr['organization'])
            return res
    else:
        return "Invalid Token"
    
@app.post("/changepass")
async def changepass(request: Request):
    data = await request.json()
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.decodeJWT(auth_token)
        if usr == 'Invalid':
            return "Invalid Token"
        else:
            id = usr['id']
            res = user_funcs.change_pass(data["otp"], id, usr['organization'], data["password"])
            return res
    else:
        return "Invalid Token"
