import openai
import os
from flask import Blueprint, request
from flask_restx import Namespace, Resource
from models import db, User, Recipe
from http import HTTPStatus

# Create a Blueprint and a Namespace
recipe_bp = Namespace('recipes', description='Recipe generation and management')

# Helper function to get the current user for demonstration
# In a real app, this would be handled by authentication (e.g., sessions, JWT)
def get_current_user():
    # For simplicity, we'll use a hardcoded user. In a real application, you would
    # get the user from the session or a token.
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        # Create a demo user if one doesn't exist
        user = User(email='demo@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
    return user

# Define the RecipeGenerator resource
@recipe_bp.route('/generate')
class RecipeGenerator(Resource):
    def post(self):
        """Generates recipes based on ingredients using OpenAI."""
        data = request.get_json()
        ingredients = data.get('ingredients')
        is_premium_request = data.get('is_premium', False)
        
        if not ingredients:
            return {'message': 'Ingredients are required'}, HTTPStatus.BAD_REQUEST

        user = get_current_user()
        
        if not user.is_premium and not is_premium_request and user.recipes_generated >= 3:
            return {
                'message': 'Free tier limit reached. Please upgrade to premium to continue.',
                'recipes_remaining': 0
            }, HTTPStatus.PAYMENT_REQUIRED
            
        try:
            # Define prompts for free and premium recipes
            if is_premium_request:
                prompt = f"Suggest 3 premium, professional-grade recipes with a Kenyan twist using the following ingredients: {ingredients}. Provide detailed nutritional information for each. Format as a structured document, separating recipes with '---'."
            else:
                prompt = f"Suggest 3 simple, easy-to-make recipes with the following ingredients: {ingredients}. Start each recipe with its title and separate each recipe with '---'."
            
            # Call OpenAI API
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1000,
                n=1,
                stop=None,
                temperature=0.7,
            )
            recipe_text = response.choices[0].text.strip()
            
            # Save the recipe to the database
            new_recipe = Recipe(user_id=user.id, ingredients=ingredients, recipe_text=recipe_text, is_premium=is_premium_request)
            db.session.add(new_recipe)
            user.recipes_generated += 1
            db.session.commit()
            
            # Return recipes and update free recipe count
            recipes = [r.strip() for r in recipe_text.split('---') if r.strip()]
            
            return {
                'recipes': recipes,
                'recipes_remaining': 3 - user.recipes_generated if not user.is_premium else -1 # -1 indicates premium
            }, HTTPStatus.OK
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error generating recipes: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR
