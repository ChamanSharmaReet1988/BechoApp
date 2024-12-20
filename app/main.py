from app.routers import user, item
from fastapi import FastAPI
from app.database import database


app = FastAPI()

# Include the user router
app.include_router(user.router)
app.include_router(item.router)


@app.get("/")
def read_root():
    database.init_db()
    return {"message": "Welcome to FastAPI!"}
