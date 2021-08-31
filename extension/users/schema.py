from extension import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','password','admin','public_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)