from flask import Flask
from flask_migrate import Migrate
from app.models import db,ma,api,Token
from app.routes import auth_bp,todo_bp
from flask_jwt_extended import JWTManager
from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=1)
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # disable CSRF for development
app.config['JWT_SECRET_KEY'] = 'c2GBkzFEXwkRTLDucE3ytW+tdEE8H4sE8eW2mbdajdQ='
app.config['JWT_ACCESS_TOKEN_EXPIRES'] =  ACCESS_EXPIRES

jwt = JWTManager(app)

api.init_app(app)
db.init_app(app)
ma.init_app(app=app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(todo_bp, url_prefix='/api/todos')

migrate = Migrate(app,db)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header,jwt_payload:dict):
    jti = jwt_payload['jti']
    token_in_db = db.session.query(Token).filter_by(token=jti).first()

    return token_in_db is not None
@app.route('/')
def home():
    return  {"Message":"Hello World"}


if __name__ == '__main__':
    app.run(debug=True)