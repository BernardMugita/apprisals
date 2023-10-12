from fastapi import FastAPI, Request
import models
import auth

app = FastAPI()

# call the create_tables() function
# create_tables() # will be done via api call


@app.get("/")
async def root():
    return ("Hello World")

@app.post("/users")
async def getallusers(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.decodeJWT(auth_token)
        if usr == "Invalid":
            return "Invalid Token"
        else:
            users = models.get_users(usr["organization"])
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
    username = data["username"]
    roles = data["roles"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    organization = data["organization"]
    telephone = data["telephone"]
    job_role = data["job_role"]
    ans = models.create_user(username, roles, first_name, last_name, email, organization, telephone, job_role)
    return ans