'''Defines a User table in the DB using SQLAlchemy ORM.

db = SQLAlchemy() sets up the ORM engine.

User class maps to users table in PostgreSQL.

Each attribute = a table column.
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def to_dict(self):
            return {
                "id": self.id,
                "username": self.username
            }