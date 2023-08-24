# Import all of our components and modules.
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

# Create the database tables. The bind parameter specifies the DB connection that
# should be used to create the tables. This value can be seen in the database.py
# file. Normally, we would use Alembic to do this initialization due to its
# capabilities and features.
models.Base.metadata.create_all(bind=engine)

# Create the app instance.
app = FastAPI()


# Now, we need to have an independent database session/connection (SessionLocal)
# per request, use that same session through all the request, and then close it
# when request is finished. A new session must be created for the next request.
# To do this, we can create a new dependency with yield, which will create a new
# SQLAlchemy SessionLocal object that will be used in a single request, and then
# close it once the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Defining our path operations
# The response_model parameter tells FastAPI that the response data should match
# the structure defined in the User pydantic model.
@app.post("/users/", response_model=schemas.User)
# The Depends(get_db) syntax is used to declare a dependency in FastAPI. First of
# all, the Depends() function is the one that declares the dependencies; it tells
# FastAPI to execute the specified functino (get_db in this case) and provide its
# return value as the value for the db parameter. In other words, here we are
# defining the functionality that we mentioned earlier (independent DB session/
# connection per request).
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        # This error will be shown to the user in a neat JSON format if the user
        # already exists.
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# Here, we are indicating that our response model will be a list of objects with
# the Pydantic model for the "User".
@app.get("/users/", response_model=list[schemas.User])
# Pretty self-explainatory so far, considering the annotations given above.
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# Setting the same response model.
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
# Here, we use the ItemCreate schema in order to have data validaton.
# Notice that this schema is the one that applies to the body of the
# request, while the one in the response_model serves as a schema for
# the response.
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


# The same as the get all users path operation.
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
