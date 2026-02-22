from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create SQLAlchemy object (NO app here)
db = SQLAlchemy()

# ---------------- USER TABLE ----------------
class User(db.Model):
    """
    Stores registered user details
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# ---------------- ADMIN TABLE ----------------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

# ---------------- ROOM TABLE ----------------
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(50))
    price = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Available")

# ---------------- BOOKING TABLE ----------------
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- PAYMENT TABLE ----------------
class Payment(db.Model):
    """
    This table stores payment information
    """
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    status = db.Column(db.String(20))   # Success / Failed
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)