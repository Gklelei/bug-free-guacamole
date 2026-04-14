from app.models import User,Todo,db
from faker import Faker
from flask_bcrypt import generate_password_hash
from main import app
import random as rd

faker = Faker()

def seed_user():
    try:
        print("Seeding Users")

        for i in range(5):
            user = User(
                name= f"{faker.first_name()} {faker.last_name()}",
                email = f"{faker.email()}",
                password = generate_password_hash("password1234").decode("utf-8")
            )
            db.session.add(user)

        db.session.commit()

        print("Users Seeded")

    except Exception as e:
        db.session.rollback()
        print("Error Seeding Users")
        print(str(e))

def seed_todo():
    try:
        todo_status = ["PENDING", "COMPLETED", "FAILED", "STARTED"]

        for i in range(10):
            todo = Todo(
                title=faker.sentence(nb_words=1),
                description= faker.sentence(nb_words=10),
                status=faker.random_element(elements=todo_status),
                user_id=rd.randint(1,5)
            )

            db.session.add(todo)

        db.session.commit()
        print("Todos Seeded")
    except Exception as e:
        db.session.rollback()
        print("Error Seeding Todos")
        print(str(e))


if __name__ == '__main__':
    with app.app_context():
        seed_user()
        seed_todo()