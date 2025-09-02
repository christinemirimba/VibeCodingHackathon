# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    is_premium = db.Column(db.Boolean, default=False)
    premium_expiry = db.Column(db.Date)
    free_recipes_remaining = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    favorites = db.relationship('UserFavorite', backref='user', lazy=True)
    ratings = db.relationship('RecipeRating', backref='user', lazy=True)
    recipe_requests = db.relationship('RecipeRequest', backref='user', lazy=True)
    
    def __init__(self, username, email, free_recipes_remaining=10, **kwargs):
        self.username = username
        self.email = email
        self.free_recipes_remaining = free_recipes_remaining
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def check_free_limit(self):
        return self.free_recipes_remaining > 0
    
    def decrement_free_limit(self):
        if self.free_recipes_remaining > 0:
            self.free_recipes_remaining -= 1
    
    def activate_premium(self, months=1):
        self.is_premium = True
        from datetime import datetime, timedelta
        self.premium_expiry = datetime.utcnow() + timedelta(days=30*months)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard'), default='Medium')
    category = db.Column(db.String(100))
    image_url = db.Column(db.String(255))
    nutritional_info = db.Column(db.JSON)
    is_premium = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ratings = db.relationship('RecipeRating', backref='recipe', lazy=True)
    favorites = db.relationship('UserFavorite', backref='recipe', lazy=True)
    
    def get_average_rating(self):
        if not self.ratings:
            return 0
        return sum(r.rating for r in self.ratings) / len(self.ratings)

class RecipeRating(db.Model):
    __tablename__ = 'recipe_ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('recipe_id', 'user_id', name='unique_rating'),
    )

class UserFavorite(db.Model):
    __tablename__ = 'user_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='unique_favorite'),
    )

class RecipeRequest(db.Model):
    __tablename__ = 'recipe_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ingredients = db.Column(db.Text, nullable=False)
    dietary_restrictions = db.Column(db.String(255))
    cuisine_type = db.Column(db.String(100))
    max_cooking_time = db.Column(db.Integer)
    status = db.Column(db.Enum('pending', 'processing', 'completed', 'failed'), default='pending')
    generated_recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    generated_recipe = db.relationship('Recipe', foreign_keys=[generated_recipe_id])

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='KES')
    payment_method = db.Column(db.String(50), default='mpesa')
    transaction_id = db.Column(db.String(255))
    status = db.Column(db.Enum('pending', 'completed', 'failed', 'refunded'), default='pending')
    description = db.Column(db.String(255))
    premium_months = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)