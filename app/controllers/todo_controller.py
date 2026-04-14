from flask_restful import Resource
from app.models import Todo,db,todo_schema,todos_schema
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import request as req
from marshmallow import ValidationError

class CreateTodoController(Resource):
    @jwt_required()
    def post(self):
        data = req.get_json()

        user_id = get_jwt_identity()

        if not data:
            return {"message": "No data provided"}, 400
        try:
            new_todo = todo_schema.load(data)
        except ValidationError as e:
            return {"error": e.messages}, 422

        try:
            new_todo.user_id = int(user_id)
            db.session.add(new_todo)
            db.session.commit()

            return {"message":"Todo Created Successfully"}, 201
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return  {"message":"Internal server error"}, 500

class GetUserTodos(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = int(get_jwt_identity())

            todos = db.session.query(Todo).filter_by(user_id=user_id).all()

            return todos_schema.dump(todos),200
        except Exception as e:
            print(str(e))
            return {"message":"Internal server error"}, 500

class DeleteTodo(Resource):
    @jwt_required()
    def delete(self,id):
        try:
            existing_todo = db.session.query(Todo).filter_by(
                id=id,
                user_id = int(get_jwt_identity())
            ).one_or_none()

            if not existing_todo:
                return {"message": f"Todo with id {id} not found or unauthorized"}, 404

            db.session.delete(existing_todo)
            db.session.commit()

            return {"message":"Todo Deleted Successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {"message":"Internal server error"}, 500

class UpdateTodo(Resource):
    @jwt_required()
    def patch(self,id):
        data = req.get_json()

        if not data:
            return {"message": "No data provided"}, 400



        try:
            todo = db.session.query(Todo).filter_by(
                id=id,
                user_id = int(get_jwt_identity())
            ).one_or_none()

            if not todo:
                return {"message": f"Todo with id {id} not found or unauthorized"}, 404

            try:
                parsed_data = todo_schema.load(data, instance=todo, partial=True)
            except ValidationError as e:
                return {"error": e.messages}, 422

            db.session.commit()

            return {"message":"Todo updated successfully","data":todo_schema.dump(parsed_data)}, 200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {"message":"Internal server error"}, 500