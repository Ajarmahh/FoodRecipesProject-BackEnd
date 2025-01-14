from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Recipes(Base):
    """
       Represents an author in the system. This model stores basic information
       about the recipes, including the name, description, ingredients and how to prepare it .
    """
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    prepare = Column(String, nullable=False)
    image = Column(String)

    def to_dict(self):
        """
        Converts the Recipes object into a dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
            "prepare": self.prepare,
            "image": self.image,
        }