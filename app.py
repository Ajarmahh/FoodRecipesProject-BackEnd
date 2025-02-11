from flask import Flask, request, jsonify
from data_manager import DataManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import config


app = Flask(__name__)
# Enable Cross-Origin Resource Sharing, allowing external clients to access the API.
CORS(app)
jwt = JWTManager(app)

data = DataManager("data/recipes.db")

app.config.from_object("config.Config")


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


@app.route('/register', methods=['POST'])
def register():
    data_reg = request.get_json()
    email = data_reg['email']
    password = data_reg['password']
    username = data_reg['username']
    # Here we simply store the password directly (no hashing)
    data.registration(email, password, username)
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data_log = request.get_json()
    email = data_log['email']
    password = data_log['password']
    user = data.authenticate(email, password)
    if not user:
        return jsonify({"message": "User not found"}), 404
    # Create a JWT access token
    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token})


@app.route('/add_recipe', methods=['POST'])
@jwt_required()
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
@jwt_required()
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
