from extension import db,app
from ..patient.models import Patient
from ..patient.schema import patient_schema,patients_schema
from extension.authorization.auth import token_required
from flask import request,jsonify
from ..patient import patient
from . import schema


@app.route('/patient',methods=['GET'])
@token_required
def get_all_patient(current_user):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})

    all_patient = Patient.query.all()
    result = patients_schema.dump(all_patient)

    return jsonify(result)

@app.route('/patient/<id>',methods=['GET'])
@token_required
def get_single_patient(current_user,id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    patient = Patient.query.get(id)

    return patient_schema.jsonify(patient)

@patient.route('/patient',methods=['POST'])
@token_required
def create_patient(current_user):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    name = request.json['name']
    age = request.json['age']
    sex = request.json['sex']
    mobile_no = request.json['mobile_no']
    weight = request.json['weight']

    new_patient = Patient(name, age, sex, mobile_no, weight)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"message": "new patient created"})

@app.route('/patient/<id>',methods=['PUT'])
@token_required
def update_patient(current_user,id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    patient = Patient.query.get(id)

    name = request.json['name']
    age = request.json['age']
    sex = request.json['sex']
    mobile_no = request.json['mobile_no']
    weight = request.json['weight']
    patient.name = name
    patient.age = age
    patient.sex = sex
    patient.mobile_no = mobile_no
    patient.weight = weight

    db.session.commit()
    return jsonify({"message":"Patient details updated"})

@app.route('/patient/<id>',methods=['DELETE'])
@token_required
def delete_patient(current_user,id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message":f"patient no. {id} deleted"})
