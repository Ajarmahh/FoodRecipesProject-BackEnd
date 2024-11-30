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
        self.session.query(Recipes.dish_name, Recipes.description, Recipes.ingredients, Recipes.image,
                           Recipes.how_to_prepare).all()
