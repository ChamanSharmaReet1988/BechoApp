from app.database.database import init_db

# Initialize the database
if __name__ == "__main__":
    init_db()
    print("Tables created successfully!")
