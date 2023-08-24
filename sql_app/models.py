# Establishing imports.
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Importing the Base class from the database.py file, so that we
# can create our DB ORM models.
from .database import Base


# Creation of the user model.
class User(Base):
    # Tells SQLAlchemy the name of the table to use in the DB for this model.
    __tablename__ = "users"
    # Each one of the next attributes represents a column in the DB table.
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # Creating a bidirectional one-to-many relationship between the User and
    # the Item models. In this case, we can access the user through the items.
    # For example, after init of an instance named "my_user", accesing
    # "my_user.items" will return a list of "Item" models (from the items table)
    # that have a foreign key pointing to a record in the users table. In other
    # words, accessing "my_user.items" causes SQLAlchemy to go and fetch the items
    # from the database in the items table and populate them here.
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    # Establishing a foreign key, where "users" in "users.id" refers to the User
    # table.
    owner_id = Column(Integer, ForeignKey("users.id"))
    # Creating a bidirectional one-to-many relationship between the User and
    # the Item models. In this case, we can access the items through the user
    # that owns them. As explained previously, accesing "my_item.owner" will
    # cause SQLAlchemy to go and fetch the items from the database in the users
    # table and populate them here.
    owner = relationship("User", back_populates="items")
