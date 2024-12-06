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
        return self.session.query(Recipes.name, Recipes.description, Recipes.ingredients, Recipes.image,
                                  Recipes.how_to_prepare).all()

    def add_recipe(self, name, description, ingredients, image, how_to_prepare):
        new_recipe = Recipes(name=name, description=description, ingredients=ingredients, image=image,
                             how_to_prepare=how_to_prepare)
        self.session.add(new_recipe)
        self.session.commit()