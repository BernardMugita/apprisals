from fastapi import FastAPI
from models import create_tables

app = FastAPI()

# call the create_tables() function
create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}
