# These models (which we'll call schemas from now on to avoid confusion
# with the SQLAlchemy schemas) define a valid data shape with data
# validation, conversion, and documentation classes and instances, all
# through type declarations.
from pydantic import BaseModel


# We create our classes which will inherit from the BaseModel, which will
# allow them to work easily with validation, serialization, and JSON schema
# generation.


# These first two classes will serve as our "base" schemas from which our
# other classes will inherit.
class ItemBase(BaseModel):
    title: str
    # The None = None declaration states that the attribute "description"
    # could either have a string value, or have a None value (which is
    # the same as being empty).
    description: str | None = None


class UserBase(BaseModel):
    email: str


# Defining the classes/models/schemas that will be used for creation.
# They inherit fromtheir respective base models, but add some attributes
# needed for the creation.
class ItemCreate(ItemBase):
    pass


class UserCreate(UserBase):
    # For security's sake, this will not be in other Pydantic models.
    # For example, it won't be sent from the API when reading a user.
    password: str


# Defining the classes/models/schemas that will be used when reading
# data and returning it from the API.
class Item(ItemBase):
    id: int
    owner_id: int

    # The behaviour of Pydantic can be controlled via the model_config
    # attribute that has as an argument the ConfigDict object. Another
    # way to do it is using the Config class.
    class Config:
        # This will tell the Pydantic model to read the data even if it
        # is not a dictionary, but an ORM model (or any other object with
        # attributes). Without this mode, if we were to return an SQLAlchemy
        # model from a path operation, it wouldn't include the relationship
        # data, even if those relationships were declared in the Pydantic
        # models. Since this will cause Pydantic to try to access the data
        # it needs from attributes (instead of assuming a dictionary form),
        # we can declare the specific data we want to return and it will be
        # able to just go and get it, even from ORMs.
        from_attributes = True


# The same things described in the previous class apply to this one.
class User(UserBase):
    id: int
    is_active: bool
    # Here, we are saying that the items attribute will have a default
    # value that equals an empty list.
    items: list[Item] = []

    class Config:
        from_attributes = True
