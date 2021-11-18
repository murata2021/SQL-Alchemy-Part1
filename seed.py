
from models import User, db
from app import app

# # Create all tables
db.drop_all()
db.create_all()

# # If table isn't empty, empty it
User.query.delete()

# # Add users

jane=User(first_name="Jane",last_name="Doe",image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLOEqJ23TlPKB9T97N50hGBRAu6sUFcqQROvXHxNdBbMVxwkPmavjJEml11_MXLw1UK2M&usqp=CAU")
joe=User(first_name="Joe",last_name="Doe")

# # Add new objects to session, so they'll persist
db.session.add(jane)
db.session.add(joe)

# # Commit--otherwise, this never gets saved!
db.session.commit()