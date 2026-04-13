from flask import Blueprint
from flask_restful import Api
from app.controllers import AuthRegisterController,AuthLoginController,AuthLogoutController,AuthValidateToken

auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)

auth_api.add_resource(AuthRegisterController, "/register", methods=["POST"])
auth_api.add_resource(AuthLoginController, "/login", methods=["POST"])
auth_api.add_resource(AuthLogoutController, "/logout", methods=["POST"])
auth_api.add_resource(AuthValidateToken, "/validate-token", methods=["GET"])

