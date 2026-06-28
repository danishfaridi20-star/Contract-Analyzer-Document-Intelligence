from flask import request,jsonify
from app.extensions import db
from ..models.user_models import User
from functools import wraps
from flask import Blueprint





user_bp = Blueprint('user',__name__)

def token_required(f):
    @wraps
    def decorated(*args,**kwargs):
        token=request.headers.get("Authorization")
        if not token or not token.startswith('Bearer'):
            return jsonify({"message":"INVALID TOKEN"})
        token=token.split()[1]
        user=User.query.filter(User.token==token).first()
        print(user)
        if not user:
            return jsonify({"message":"invalid token"})
        return f(*args,**kwargs,current_user=user)
    return decorated

@user_bp.route('/userlogin',methods=["POST"])
def hybrid_login():
    data=request.get_json()
    user=User.query.filter(User.user_name==data["user_name"]).first()
    if user and user.password_hash == data["password_hash"]:
        User.set_token(user) 
        db.session.commit()
        return jsonify({"token":user.token} )
    return jsonify({"message":"invalid"})

@token_required
@user_bp.route('/userlogout', methods=["GET"])
def hybrid_logout(current_user):
    current_user.token=None
    db.session.commit()
    return jsonify({"message":"logout successfully"})

@user_bp.route('/getuser',methods=["GET"])
def get_user():
    data=[
    {
         
        "id":g.id,
        "user_name":g.user_name,
        "email":g.email,
        "password_hash":g.password_hash,
        "phone_number":g.phone_number
        
    }for g in (User.query.all())
    ]
    return jsonify(data)

@user_bp.route('/getsuser/<int:id>',methods=["GET"])
def get_userby_id(id):
    data=[
    {
         
        "id":f.id,
        "user_name":f.user_name,
        "email":f.email,
        "password_hash":f.password_hash,
        "phone_number":f.phone_number
        
    }for f in User.query.filter(User.id==id).all()
    ]
    return jsonify(data)

@user_bp.route('/getsuser/<string:user_name>',methods=["GET"])
def get_userby_name(user_name):
    data=[
    {
         
        "id":f.id,
        "user_name":f.user_name,
        "email":f.email,
        "password_hash":f.password_hash,
        "phone_number":f.phone_number
        
    }for f in User.query.filter(User.user_name==user_name).all()
    ]
    return jsonify(data)


@user_bp.route('/postsuser',methods=["POST"])
def posts_user():
    data=request.get_json()
    users=User(user_name=data["user_name"],email=data["email"],password_hash=data["password_hash"],phone_number=data["phone_number"])
    db.session.add(users)
    db.session.commit()
    return jsonify({"message":"user posted successfully "})


@user_bp.route('/putsuser/<int:id>',methods=["PUT"])
def put_user():
    user=User.query.get(id)
    data=request.get_json()
    user.user_name=data.get("user_name",user.user_name)
    user.email=data.get('email',user.email)
    user.password_hash=data.get('passwords_hash')
    db.session.commit()
    return jsonify({"message":"updated successfully"})   

@user_bp.route('/deluser/<int:id>',methods=["DELETE"])
def del_user(id):
    result=User.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return ({"message":"user deleted"})