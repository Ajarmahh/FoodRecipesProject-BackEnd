from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
from data_models import Base, Recipes, Users, Admin


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

    def add_recipe(self, name, description, ingredients, image, prepare):
        new_recipe = Recipes(name=name, description=description, ingredients=ingredients, image=image,
                             prepare=prepare)
        self.session.add(new_recipe)
        self.session.commit()

    def delete_recipe(self, recipe_id):
        recipe = self.session.query(Recipes).get(recipe_id)
        if recipe:
            self.session.delete(recipe)
            self.session.commit()

    def authenticate(self, email, password):
        """
        Authenticate a user or admin by email and password.
        Returns the authenticated entity (user or admin) if successful, otherwise None.
        """
        # Check if the email exists in the users table
        user = self.session.query(Users).filter_by(email=email).first()
        if not user:
            return {"msg": "User not found"}

            # Ensure password verification
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return {'entity': user, 'role': 'user'}

        # Check if the email exists in the admins table
        # admin = self.session.query(Admin).filter_by(email=email).first()
        # if admin and check_password_hash(admin.password, password):
        #     return {'entity': admin, 'role': 'admin'}

        return {"msg": "Invalid user"}

    def registration(self, email, password, username):
        """
        Authenticate a user or admin by email and password.
        Returns the authenticated entity (user or admin) if successful, otherwise None.
        """
        # Check if the email exists in the users table
        user = self.session.query(Users).filter_by(email=email).first()
        if user:
            return {"msg": "user exist"}
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create new user with hashed password
        new_user = Users(email=email, password=hashed_password.decode('utf-8'), username=username)
        self.session.add(new_user)
        self.session.commit()

        return {"msg": "User registered successfully"}
