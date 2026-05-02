"""
Run this once to create the default admin user:
    python create_admin.py
"""
from database import engine, get_db
import models
import schemas
import crud

# Create tables if they don't exist yet
models.Base.metadata.create_all(bind=engine)

db = next(get_db())

USERNAME = "admin"
PASSWORD = "admin123"

existing = crud.get_user_by_username(db, USERNAME)
if existing:
    print(f"User '{USERNAME}' already exists.")
else:
    crud.create_user(db, schemas.UserCreate(username=USERNAME, password=PASSWORD))
    print(f"Admin user created — username: {USERNAME}  password: {PASSWORD}")
