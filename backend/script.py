from app import app, db
from models import Users, Application

with app.app_context():
    db.create_all()