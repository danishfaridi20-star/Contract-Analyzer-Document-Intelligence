from app.extensions import db
import secrets
from sqlalchemy.sql.schema import ForeignKey

class Term_conditions(db.Model):
    __tablename__='term_conditions'
    id=db.Column(db.Integer,primary_key=True)
    user=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)
    content=db.Column(db.Text,nullable=True)
    product_name=db.Column(db.String(255),nullable=True)
    product_company=db.Column(db.String(255),nullable=True)
    summary= db.Column(db.Text,nullable=True)
    def set_token(self):
        self.token=secrets.token_hex(32)
        print(self.token)
    