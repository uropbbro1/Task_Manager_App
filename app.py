import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import bcrypt

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_default_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///site.db")  # Use sqlite for simplicity
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
from routes import *
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)