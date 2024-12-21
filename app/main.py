from app.routers import user, item
from fastapi import FastAPI
from app.database import database
from sqladmin import Admin, ModelView
from app.models.user_model import User
from app.models.items_model import Item

app = FastAPI()
admin = Admin(app, database.engine)

# Include the user routerpip install --upgrade aioredis
app.include_router(user.router)
app.include_router(item.router)


@app.get("/")
def read_root():
    database.init_db()
    return {"message": "Welcome to FastAPI!"}


# For admin part
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.phone]


class ItemAdmin(ModelView, model=Item):
    column_list = [Item.id, Item.title,
                   Item.description, Item.price, Item.views]


admin.add_view(UserAdmin)
admin.add_view(ItemAdmin)
