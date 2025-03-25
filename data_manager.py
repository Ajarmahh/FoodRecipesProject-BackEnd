from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
from data_models import Base, Recipes, Users, Admins


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

    def add_recipe(self, name, description, ingredients, image, prepare, user_id):
        new_recipe = Recipes(name=name, description=description, ingredients=ingredients, image=image,
                             prepare=prepare, user_id=user_id, status="pending")
        self.session.add(new_recipe)
        self.session.commit()

    def delete_recipe(self, recipe_id):
        recipe = self.session.query(Recipes).get(recipe_id)
        if recipe:
            self.session.delete(recipe)
            self.session.commit()

    def authenticate_admin(self, email, password):
        admin = self.session.query(Admins).filter_by(email=email).first()

        if admin:
            # Ensure password verification for admins
            if bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
                return {'entity': admin, 'role': 'admin'}
            return None

    def authenticate(self, email, password):
        """
        Authenticate a user or admin by email and password.
        Returns the authenticated entity (user or admin) if successful, otherwise None.
        """
        # Check if the email exists in the users or admins table
        user = self.session.query(Users).filter_by(email=email).first()

        if user:
            # Ensure password verification for users
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return {'entity': user, 'role': 'user'}
            return None

    def registration(self, email, password, username):
        """
        Authenticate user by email and password.
        Returns the authenticated entity user if successful, otherwise None.
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

    def admin_only_users(self, email=None):
        """
        Fetches all users if the provided email belongs to an admin.
        """
        if email:
            # Check if the email belongs to an admin
            admin = self.session.query(Admins).filter_by(email=email).first()
            if not admin:
                return "You are not authorized", 403

        # Fetch all users
        users = self.session.query(Users).all()
        user_list = [user.to_dict() for user in users]

        return user_list, 200

    def delete_user_by_id(self, user_id):
        """
        Deletes a user by their ID.
        """
        user = self.session.query(Users).filter_by(id=user_id).first()
        if not user:
            return "User not found", 404

        self.session.delete(user)
        self.session.commit()
        return "User deleted successfully", 200

    def make_user_admin(self, user_id):
        """
        Promotes a user to an admin by their ID and removes them from the Users table.
        """
        user = self.session.query(Users).filter_by(id=user_id).first()
        if not user:
            return "User not found", 404

        # Check if the user is already an admin
        admin = self.session.query(Admins).filter_by(email=user.email).first()
        if admin:
            return "User is already an admin", 400

        hashed_password = user.password  # Use the existing hashed password from the Users table

        # Create a new admin entry
        new_admin = Admins(username=user.username, email=user.email, password=hashed_password)
        self.session.add(new_admin)

        # Delete the user from the Users table
        self.session.delete(user)

        self.session.commit()

        return "User promoted to admin successfully", 200
