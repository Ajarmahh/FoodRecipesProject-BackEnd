from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_models import Base, Recipes


class DataManager:
    def __init__(self, db_file_name):
        # Create the engine (adjust the database URL as needed)
        self.engine = create_engine(f'sqlite:///{db_file_name}')

        # Create a new session maker bound to the engine
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Create all tables defined in the Base class
        Base.metadata.create_all(self.engine)

    def get_data(self):
        recipes = self.session.query(Recipes).all()
        return [recipe.to_dict() for recipe in recipes]

    def add_recipe(self, name, description, ingredients, image, .prepare):
        new_recipe = Recipes(name=name, description=description, ingredients=ingredients, image=image,
                             prepare=prepare)
        self.session.add(new_recipe)
        self.session.commit()

    def delete_recipe(self, recipe_id):
        recipe = self.session.query(Recipes).get(recipe_id)
        if recipe:
            self.session.delete(recipe)
            self.session.commit()