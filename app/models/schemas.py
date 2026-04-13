from app.models import db,User, ma,Todo

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field(load_only=True)

class TodoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Todo
        load_instance = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field()
    description = ma.auto_field()
    status = ma.auto_field()
    user_id = ma.auto_field()