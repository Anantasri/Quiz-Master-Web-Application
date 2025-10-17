from flask_security import SQLAlchemyUserDatastore
from backend.models import User,Role
from backend.database import db

user_datastore = SQLAlchemyUserDatastore(db,User,Role)
