from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



engine = create_engine('postgresql://postgres:zeal@localhost:5432/robin')
Base = declarative_base()



# Import the model definition here
from .models import *
Base.metadata.create_all(engine)

# Create a session for database operations
Session = sessionmaker(bind=engine)
session = Session()
