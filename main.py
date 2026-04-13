from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app)

@app.route('/')
def home():
    return  {"Message":"Hello World"}


if __name__ == '__main__':
    app.run(debug=True)