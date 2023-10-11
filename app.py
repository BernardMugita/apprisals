from fastapi import FastAPI, Request
import models

app = FastAPI()

# call the create_tables() function
# create_tables() # will be done via api call


@app.get("/")
async def root():
    return ("Hello World")

@app.post("/users")
async def getallusers(request: Request):
    data = await request.json() # we will get this from decodeJWT
    users = models.get_users(data["company"])
    return users