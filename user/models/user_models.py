from app.extensions import db
import secrets

class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(255),unique=True,nullable=False)
    email=db.Column(db.String(255),unique=True,nullable=False)
    password_hash=db.Column(db.String(255),unique=True,nullable=False)
    phone_number=db.Column(db.String(255),unique=True,nullable=False)
    token=db.Column(db.String(255),unique=True)

    def set_token(self):
        self.token=secrets.token_hex(32)
        print(self.token)