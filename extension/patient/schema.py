from extension import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','age','sex','weight','mobile_no.','time')

patient_schema = UserSchema()
patients_schema = UserSchema(many=True)