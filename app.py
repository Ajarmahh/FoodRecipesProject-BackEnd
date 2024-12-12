from flask import Flask, render_template, request, redirect, url_for, jsonify
from data_manager import DataManager
from flask_cors import CORS

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing, allowing external clients to access the API.
CORS(app)
# Configure CORS to allow requests only from the specified origin, running on localhost: 3000
CORS(app, resources={r"/*": {"origins": "<http://localhost:3000>"}})

data = DataManager("data/recipes.db")


@app.route('/', methods=['GET'])
def get_recipes():
    """
    Fetch and display all recipes from the database.
    """
    try:
        # Retrieve all recipes from the database.
        recipes = data.get_data()
        return jsonify(recipes)
    except Exception as e:
        return jsonify({"error": f"Error fetching recipes: {e}"}), 500


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    """
    Handle adding a new recipe to the database.
    """
    try:
        # Extract recipe details from the submitted form.
        # name = request.form.get('name')
        name = request.json['name']
        description = request.json['description']
        ingredients = request.json['ingredients']
        image = request.json['image']
        how_to_prepare = request.json['how_to_prepare']

        # Add the new recipe to the database.
        data.add_recipe(name, description, ingredients, image, how_to_prepare)
        return jsonify({"message": "Recipe added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Error adding recipe: {e}"}), 500


@app.route('/delete_recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """
    Handle deletion of a recipe by its ID.
   """
    try:
        data.delete_recipe(recipe_id)
        return f'Recipe num {recipe_id} Deleted'
    except Exception as e:
        return e


if __name__ == '__main__':
    app.run(port=4000 ,debug=True)
