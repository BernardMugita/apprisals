from fastapi import FastAPI, Request
from routers import task_routes, user_routes, pslips_routes
import models
import company_funcs
import auth

app = FastAPI()

app.include_router(task_routes.router)
app.include_router(user_routes.router)
app.include_router(pslips_routes.router)

# call the create_tables() function
# create_tables() # will be done via api call


@app.get("/")
async def root():
    return ("Habari kutoka Nairobi")


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
    ans = company_funcs.create_company(company, email, telephone, address, city, country, domain)
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
            ans = company_funcs.create_company_tables(company)
            return ans
    else:
        return "Invalid Token"
    
# @app.post("/clear_redis_company")
# async def clear_redis(request: Request):
#     data = await request.json()
#     company = data["company"]
#     auth_header = request.headers.get('Authorization')
#     if auth_header and auth_header.startswith("Bearer "):
#         auth_token = auth_header.split(" ")[1]
#         usr = auth.check_superadmin_JWT(auth_token)
#         if usr == False:
#             return "Invalid Token"
#         else:
#             ans = company_funcs.clear_redis(company)
#             return ans
#     else:
#         return "Invalid Token"

@app.get("/clear_redis_all")
def clear_redis_all(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        auth_token = auth_header.split(" ")[1]
        usr = auth.check_superadmin_JWT(auth_token)
        if usr == False:
            return "Invalid Token"
        else:
            ans = user_routes.redis_funcs.redis_clear_all()
            return ans
    else:
        return "Invalid Token"
