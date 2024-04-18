from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import app
import re

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.String(15))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip = db.Column(db.String(10))
    role = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, default=1000.0)
    ratings = db.relationship('ContentReview', backref='rater', lazy=True)

    def validate_username(self, username):
        if len(username) > 20:
            raise ValueError("Username must be at most 20 characters long.")

    def validate_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search("[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search("[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search("[0-9]", password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search("[!@#$%^&*()-_+=]", password):
            raise ValueError("Password must contain at least one special character.")

    def validate_state(self, state):
        if re.search("[^a-zA-Z\s]", state):
            raise ValueError("State name can only contain alphabets and spaces.")

class ContentReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    image = db.Column(db.LargeBinary)
    imageType = db.Column(db.String(10))
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ratings = db.relationship('ContentReview', backref='content', lazy=True)
    number_of_pages = db.Column(db.Integer, nullable=False)
    publish_year = db.Column(db.Integer, nullable=False)
    file = db.Column(db.LargeBinary, nullable=False)
    pdf_file_name = db.Column(db.String(250), nullable=True)
    price = db.Column(db.Float, nullable=False)
    section = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    borrowings = db.relationship('Borrowing', backref='borrowed_content', lazy=True)
    wishlists = db.relationship('Wishlist', backref='wishlisted_content', lazy=True)

class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    content_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)

class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    returned = db.Column(db.Boolean, default=False)
    return_date = db.Column(db.DateTime)
    last_return_date = db.Column(db.DateTime)
    reissue_count = db.Column(db.Integer, default=0)
    is_read = db.Column(db.Boolean, default=False)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    user = db.relationship('User', backref='wishlist_items', lazy=True)
    content = db.relationship('Content', back_populates='wishlists', lazy=True, overlaps="wishlisted_content")

class LoginData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_login_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

class PurchaseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)

class IssueRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contentId = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    response = db.Column(db.String(10), default='Pending')