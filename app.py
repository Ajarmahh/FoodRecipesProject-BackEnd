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
    try:
        recipes = data.get_data()
        return render_template('home.html', recipes=recipes)
    except Exception as e:
        return render_template('home.html', error=e)


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description')
            ingredients = request.form.get('ingredients')
            image = request.form.get('image')
            how_to_prepare = request.form.get('how_to_prepare')
            data.add_recipe(name, description, ingredients, image, how_to_prepare)
            return redirect(url_for('get_recipes'))
        except Exception as e:
            print(f'Error adding recipe: {e}')
    return render_template('add_recipe.html')


@app.route('/delete_recipe/<int:recipe_id>')
def delete_recipe(recipe_id):
    try:
        data.delete_recipe(recipe_id)
        return redirect(url_for('get_recipes'))
    except Exception as e:
        data.session.rollback()
        print(f'Error deleting recipe: {e}')


if __name__ == '__main__':
    app.run(debug=True)
