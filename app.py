from flask import Flask, request, jsonify
from data_manager import DataManager
from flask_cors import CORS

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing, allowing external clients to access the API.
CORS(app)

# Enable CORS to allow requests from http://localhost:5173
CORS(app)

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
        prepare = request.json['prepare']

        # Add the new recipe to the database.
        data.add_recipe(name, description, ingredients, image, prepare)
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
    app.run(host="0.0.0.0", port=4000, debug=True)
