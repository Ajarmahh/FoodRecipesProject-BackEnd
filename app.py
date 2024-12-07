from flask import Flask, render_template, request, redirect, url_for
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
        return render_template('home.html', recipes=recipes)
    except Exception as e:
        print(f'print error: {e}')
        return render_template('home.html', error=e)


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    """
    Handle adding a new recipe to the database.
    """
    if request.method == 'POST':
        try:
            # Extract recipe details from the submitted form.
            name = request.form.get('name')
            description = request.form.get('description')
            ingredients = request.form.get('ingredients')
            image = request.form.get('image')
            how_to_prepare = request.form.get('how_to_prepare')

            # Add the new recipe to the database.
            data.add_recipe(name, description, ingredients, image, how_to_prepare)
            return redirect(url_for('get_recipes'))
        except Exception as e:
            print(f'Error adding recipe: {e}')
    return render_template('add_recipe.html')


@app.route('/delete_recipe/<int:recipe_id>')
def delete_recipe(recipe_id):
    """
    Handle deletion of a recipe by its ID.
    """
    try:
        data.delete_recipe(recipe_id)
        return redirect(url_for('get_recipes', recipe_id=recipe_id))
    except Exception as e:
        # Rollback the database session in case of an error and log the issue.
        data.session.rollback()
        print(f'Error deleting recipe: {e}')


# Catch 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', error=error), 404


# Catch server side errors
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', error=error), 500


# Catch all the other exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {e}")
    return render_template("errors/error.html", error="An unexpected error occurred.", exception=e), 500


if __name__ == '__main__':
    app.run(debug=True)
