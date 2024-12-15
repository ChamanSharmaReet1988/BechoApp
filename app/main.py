from fastapi import FastAPI
from app.routers import user
from app.database.database import init_db

app = FastAPI()

# Include the user router
app.include_router(user.router)


@app.get("/")
def read_root():
    # init_db()
    return {"message": "Welcome to FastAPI!"}
