from flask import Flask, jsonify, request
from app.model import User
from app.serializer import UserSchema, UpdateUserSchema
from app_init.app_factory import create_app
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os

settings_name = os.getenv("settings")
app = create_app(settings_name)

@app.route('/users', methods=["POST"])
def create_user():
    user_info = request.get_json()
    user = User.query.filter_by(email=user_info.get("email")).first()
    if user:
        return jsonify(msg="User exists"),HTTPStatus.BAD_REQUEST
    try:
        data = UserSchema().load(user_info)
        data.generate_password()
        data.save_db()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return UserSchema().jsonify(data),HTTPStatus.OK

@app.route('/users', methods=["GET"])
@jwt_required
def get_user():
    identity = get_jwt_identity()
    user_info = User.query.filter_by(email=identity).first()
    return UserSchema().jsonify(user_info),HTTPStatus.OK

@app.route('/users/login', methods=["POST"])
def user_login():
    user_info = request.get_json()
    user : User= User.query.filter_by(email=user_info.get("email")).first()
    if user:
        if user.chech_password(user_info.get("password")):
            access_token = create_access_token(identity=user.email)
            user_schema = UserSchema().dump(user)
            user_schema["access_token"] = access_token
            return jsonify(user_schema),HTTPStatus.OK
    return jsonify(msg="Incorrect email or password"),HTTPStatus.NOT_FOUND  


@app.route('/users', methods=["DELETE"])
@jwt_required
def delete_user():
    identity = get_jwt_identity()
    user_info = User.query.filter_by(email=identity).first()
    user_info.delete_from_db()
    return jsonify(msg="OK"),HTTPStatus.OK

@app.route('/users', methods=["PUT"])
@jwt_required
def update_user():
    identity = get_jwt_identity()
    user_info = User.query.filter_by(email=identity).first()
    if user_info:
        new_user = request.get_json()
        new_user = UpdateUserSchema().load(new_user)
        user_info.update_db(**new_user)
        return UserSchema().jsonify(user_info),HTTPStatus.OK
    return jsonify(msg="Not found"),HTTPStatus.OK




    
 