from fastapi import FastAPI
from app.routers import user

app = FastAPI()

# Include the user router
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
