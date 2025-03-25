from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
import enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Admins(Base):
    """
    Represents an admin in the system. This model stores admin-specific information,
    including name, email, hashed password, and admin status.
    """
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def to_dict(self):
        """
        Converts the Admin object into a dictionary.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class Users(Base):
    """
       Represents a user in the system. This model stores user information,
       including name, email, and hashed password.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)  # Ensure email is unique
    password = Column(String, nullable=False)

    def to_dict(self):
        """
        Converts the Users object into a dictionary.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class RecipeStatusEnum(enum.Enum):
    """
    Enum representing the possible statuses of a recipe.
    """
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Recipes(Base):
    """
       Represents a recipe in the system. This model stores basic information
       about the recipe, including the name, description, ingredients, and preparation method.
    """
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    prepare = Column(String, nullable=False)
    image = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key linking the recipe to a user
    status = Column(Enum(RecipeStatusEnum), default=RecipeStatusEnum.pending)

    def to_dict(self):
        """
        Converts the Recipes object into a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
            "prepare": self.prepare,
            "image": self.image,
            "user_id": self.user_id,
            "status": self.status.value,
        }


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  # Name of the person commenting
    comment_text = Column(String, nullable=False)
    #comment_time = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))  # Default to current time
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Links comment to a user
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)  # Links comment to a recipe
