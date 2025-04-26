#App Setup
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes import bp
from config import DB_URI, JWT_SECRET

app = Flask(__name__)

# Configuration - Sets up DB and JWT secret for Flask.
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET

''' Initialize DB & JWT
Links the DB and JWT to Flask app
Registers your API routes
'''
db.init_app(app)
with app.app_context():
    db.create_all()

JWTManager(app)
app.register_blueprint(bp)

# Start the app on port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
