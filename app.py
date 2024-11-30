from flask import Flask, render_template
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


if __name__ == '__main__':
    app.run(debug=True)