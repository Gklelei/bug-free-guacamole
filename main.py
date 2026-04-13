from flask import Flask
from flask_migrate import Migrate
from app.models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app,db)

@app.route('/')
def home():
    return  {"Message":"Hello World"}


if __name__ == '__main__':
    app.run(debug=True)