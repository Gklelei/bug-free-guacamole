from flask import request as req, make_response
from flask_restful import Resource
from app.models import user_schema, db, User, Token
from marshmallow import ValidationError
from flask_bcrypt import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,get_jwt



class AuthRegisterController(Resource):
    def post(self):
        data = req.get_json()

        if not data:
            return {"message": "No data provided"}, 400

        try:
            new_user = user_schema.load(data)
        except ValidationError as e:
            return {"message": e.messages}, 422

        try:
            existing_user = db.session.query(User).filter_by(email=new_user.email).one_or_none()

            if existing_user:
                return {"message": "User already exists"}, 409

            new_user.password = generate_password_hash(new_user.password).decode('utf-8')

            db.session.add(new_user)
            db.session.commit()
            return {"message": "User created successfully"}, 201

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {"message": "Internal server error"}, 500

class AuthLoginController(Resource):
    def post(self):
        data = req.get_json()

        if not data:
            return {"message": "No data provided"}, 400

        try:
            user_info = user_schema.load(data,partial=True)

        except ValidationError as e:
            return  {"message": e.messages}, 422

        try:
            existing_user = db.session.query(User).filter_by(email=user_info.email).one_or_none()

            if not existing_user:
                return {"message": "Invalid Credentials"}, 400

            is_Pwd_match = check_password_hash(existing_user.password, user_info.password)

            if not is_Pwd_match:
                return {"message": "Invalid Credentials"}, 401

            token = create_access_token(identity=str(existing_user.id))

            response = make_response({"message":"Login successful"}, 200)
            response.set_cookie(
                "access_token_cookie",
                token,
                httponly=True,
                secure=False,
                samesite="Strict",
                max_age=3600
            )

            return  response
        except Exception as e:
            print(str(e))
            return {"message": "Internal server error"}, 500





class AuthLogoutController(Resource):
    @jwt_required()  # note the () — jwt_required is a decorator factory
    def post(self):
        try:
            jti = get_jwt()["jti"]
            token = Token(token=jti)
            db.session.add(token)
            db.session.commit()

            response = make_response({"message": "Logout successful"}, 200)
            response.delete_cookie("token")
            return response

        except Exception as e:
            print(str(e))
            return {"message": "Internal server error"}, 500

class AuthValidateToken(Resource):
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        try:
            user = db.session.get(User,int(id))
            return user_schema.dump(user)
        except Exception as e:
            print(str(e))
            return {"message": "Internal server error"}, 500
