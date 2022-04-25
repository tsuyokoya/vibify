from models import db, User

# Add a User
user_one = User.register(first_name="Bob", email="bob@gmail.com", password="hello")

db.session.commit()
