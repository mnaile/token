from extensions.extensions import db
from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    __tablename__="userlogin"

    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(), nullable = True)
    password = db.Column(db.String(), nullable = True)

    def generate_password(self):
        self.password = generate_password_hash(self.password)

    def chech_password(self, password_hash):
        return check_password_hash(self.password, password_hash)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save_db()