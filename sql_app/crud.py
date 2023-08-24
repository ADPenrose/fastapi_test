# Here, we will have reusable functions that allow us to interact
# with the data in the DB. This allows us to reuse them in multiple
# parts of our path operation functions, and also add unit tests
# for them.

# This import will allow us to declare the type of the DB parameters
# and have better type checks and completitions.
from sqlalchemy.orm import Session

# This import will allow us to use all of the structures declared in
# the specified files present in this folder.
from . import models, schemas


# Read a single user by ID.
def get_user(db: Session, user_id: int):
    # The db.query() function creates an initial query object that targets
    # the "User" model. In essence, it is saying "I want to query the 'User'
    # table in the DB". Then the filter() function adds a filter to the
    # query, specifying that we want to retrieve a user whose id matches
    # the user_id argument passed to the function (like the WHERE clause
    # in SQL). Finally, the first() function retrieves the first result that
    # matches the given conditions (equivalent to SQL's SELECT ... LIMIT 1).
    return db.query(models.User).filter(models.User.id == user_id).first()


# Read a single user by email.
def get_user_by_email(db: Session, email: str):
    # The workings of this line are the same than those of the previous
    # function, with the difference that we are filtering by the email.
    return db.query(models.User).filter(models.User.email == email).first()


# Read all users.
# The skip parameter (which has a default value of 0) represents the number
# of records to skip when fetching the results. It allows for pagination
# (allows us to present large datasets in smaller, more manageble chunks,
# which are called pages. Especially useful when we are dealing with DB
# too large to be displayed or processed at once). Here, we are using it
# in conjunction with the offset() method to indicate that we want to start
# getting users from the first page.The limit parameter (with a default
# value of 100), in conjunction with the limit() method, indicates the
# maximum number of records to retrieve in a single query.
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # This creates a query object that targets the User model. Then, we
    # specify an offset to the query, indicating it how many records it
    # should skip. E.g. if skip = 10, the query will start retrieving
    # records from the 11th one onwards. As mentioned earlier, in this
    # case it starts from the beginning. The limit() method specifies
    # the max. number of results that the query will retrieve. Finally,
    # the all() method will return all of the results that match the
    # query in form of a list.
    return db.query(models.User).offset(skip).limit(limit).all()


# Read all items.
def get_items(db: Session, skip: int = 0, limit: int = 100):
    # The exact same working principle as the function above.
    return db.query(models.Item).offset(skip).limit(limit).all()


# Create a user.
# The user parameter will only accept a UserCreate pydantic schema. This
# will provide useful data validation.
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "noreallyahash"
    # Create an instance of the user model.
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # Add our new user to the current DB session. However, it is not yet inserted;
    # it is just staged for insertion.
    db.add(db_user)
    # This will commit the transaction, effectively inserting the user into the DB.
    db.commit()
    # The refresh() method will refresh the state of the "db_user" object with the
    # state of that object in the DB. This will allow us to access any new data added
    # in the DB, like the generated ID.
    db.refresh(db_user)
    return db_user


# Create a user item.
# Exact same funcionality as the function above.
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
