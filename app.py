from flask import Flask, render_template, request, jsonify
import json
import os
import random
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load recipes and additional data from external JSON file
def load_data():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'recipes.json'), 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logging.error("Error: recipes.json file not found.")
        return {
            "recipes": {},
            "cooking_tips": [],
            "food_facts": [],
            "cooking_questions": {}
        }
    except json.JSONDecodeError:
        logging.error("Error: recipes.json file contains invalid JSON.")
        return {
            "recipes": {},
            "cooking_tips": [],
            "food_facts": [],
            "cooking_questions": {}
        }

data = load_data()  # Load the data at app startup

@app.route('/')
def render_homepage():
    """Renders the main page for the chatbot interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def process_chat():
    """Handles incoming chat messages and generates responses."""
    user_message = request.json.get('message', '').strip()  # Get the message and strip whitespace
    if not user_message:  # Validate the input
        return jsonify({"response": "Please enter a message."}), 400

    bot_reply = generate_response(user_message)
    return jsonify({"response": bot_reply})

def generate_response(user_message):
    """Generates a response based on user input."""
    user_message_lower = user_message.lower()

    # Check for recipes
    for dish in data.get('recipes', {}):
        if dish in user_message_lower:
            return format_recipe(dish)

    # Check for cooking tips
    if "tip" in user_message_lower:
        return f"**Cooking Tip:**\n\n{random.choice(data.get('cooking_tips', ['I don’t have a tip right now, but feel free to ask about recipes!']))}"

    # Check for food facts
    if "fact" in user_message_lower or "did you know" in user_message_lower:
        return f"**Food Fact:**\n\n{random.choice(data.get('food_facts', ['I’m here to provide recipes, tips, and facts! Just let me know what you need.']))}"

    # Check for common cooking questions
    for question, answer in data.get('cooking_questions', {}).items():
        if question in user_message_lower:
            return f"**Answer:**\n\n{answer}"

    # Default response if nothing matches
    return "I'm here to help! Ask me for a recipe, a cooking tip, or even a food fact."

def format_recipe(dish):
    """Formats the recipe response for a specific dish."""
    recipe = data['recipes'].get(dish)
    if recipe:
        # Creating HTML formatted ingredients and steps
        ingredients = "".join([f"<li>{ingredient}</li>" for ingredient in recipe["ingredients"]])
        steps = "".join([f"<p>{i + 1}. {step}</p>" for i, step in enumerate(recipe["steps"])])

        return (
            f"<h3>Recipe for {dish.capitalize()}</h3>"
            f"<strong>Ingredients:</strong><ul>{ingredients}</ul>"
            f"<strong>Steps:</strong>{steps}"
        )
    else:
        return f"<p>Sorry, I don't have a recipe for {dish}.</p>"

if __name__ == '__main__':
    app.run(debug=True)
