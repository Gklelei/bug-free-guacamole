from flask_restful import Api
from flask import Blueprint
from app.controllers import CreateTodoController, GetUserTodos, DeleteTodo, UpdateTodo

todo_bp = Blueprint('todo_bp', __name__)
api = Api(todo_bp)

api.add_resource(CreateTodoController, "/", methods=["POST"])
api.add_resource(GetUserTodos, "/", methods=["GET"])
api.add_resource(DeleteTodo, "/<int:id>", methods=["DELETE"])
api.add_resource(UpdateTodo, "/<int:id>", methods=["PATCH"])