from fastapi import FastAPI, Request
from routers import task_routes, user_routes
import models
import user_funcs
import auth

app = FastAPI()

app.include_router(task_routes.router)
app.include_router(user_routes.router)

# call the create_tables() function
# create_tables() # will be done via api call


@app.get("/")
async def root():
    return ("Hello from Nairobi")


@app.post("/createcompany")
async def createcompany(request: Request):
    #header authoarization check
    data = await request.json()
    company = data["company"]
    domain = data["domain"]
    email = data["email"]
    telephone = data["telephone"]
    address = data["address"]
    city = data["city"]
    country = data["country"]
    ans = models.create_company(company, email, telephone, address, city, country, domain)
    return ans


@app.post("/createcompanytables")
async def createcompanytables(request: Request):
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
    

