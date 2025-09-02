import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Note: The 'IntaSend' library is not a standard Python library,
# so you'll need to replace this with the actual library you use for Intasend.
# For example: 'from intasend import IntaSend'
# from intasend import IntaSend

# Import the Config class from your config.py file
from config import Config

# Load environment variables from .env file
load_dotenv()

# Create a Flask application instance and load the configuration
app = Flask(__name__)
app.config.from_object(Config)

# Get the API keys directly from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
intasend_secret_key = os.getenv("INTASEND_SECRET_KEY")
intasend_publishable_key = os.getenv("INTASEND_PUBLISHABLE_KEY")

# Add print statements to verify the keys are loaded
print(f"Loaded OpenAI API Key: {openai_api_key}")
print(f"Loaded Intasend Secret Key: {intasend_secret_key}")
print(f"Loaded Intasend Publishable Key: {intasend_publishable_key}")


if not openai_api_key:
    print("Error: OpenAI API key is not configured. Please check your .env file.")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Placeholder for Intasend client initialization
# intasend_client = IntaSend(secret_key=intasend_secret_key, publishable_key=intasend_publishable_key)

# Function to get a database connection
def get_db_connection():
    # Use a direct filename since your config doesn't provide a URL for a simple file-based DB
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to serve the main index.html file.
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the recipe search and AI suggestion
@app.route('/search_recipes', methods=['POST'])
def search_recipes():
    data = request.json
    ingredients = data.get('ingredients')

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    prompt = f"Suggest 3 simple recipes with the following ingredients: {', '.join(ingredients)}. Format the response as a JSON array of objects, where each object has 'label', 'ingredientLines', and 'url' fields."

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        response_text = completion.choices[0].message.content
        recipes = eval(response_text)

        conn = get_db_connection()
        for recipe in recipes:
            conn.execute('INSERT INTO recipes (label, ingredientLines, url) VALUES (?, ?, ?)',
                         (recipe['label'], ', '.join(recipe['ingredientLines']), recipe['url']))
        conn.commit()
        conn.close()

        return jsonify(recipes)

    except Exception as e:
        # Print the detailed error to the terminal for debugging
        print(f"Error during recipe search: {e}")
        return jsonify({"error": "Something went wrong. Please try again."}), 500

# Placeholder for an Intasend-related route
# @app.route('/initiate_payment', methods=['POST'])
# def initiate_payment():
#     # This is where you would handle the payment logic with Intasend
#     # For example:
#     # response = intasend_client.checkout(...)
#     # return jsonify(response)
#     pass

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
