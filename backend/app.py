from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, User, Application

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY

CORS(app)
db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()

# 认证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = User.query.filter_by(username=username, role=role).first()
    if user and user.check_password(password):
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid username, password or role'}), 401

# 获取申请列表接口
@app.route('/api/applications', methods=['GET'])
@token_required
def get_applications(current_user):
    applications = Application.query.all()
    output = []
    for app in applications:
        app_data = {}
        app_data['id'] = app.id
        app_data['student_name'] = app.student_name
        app_data['university'] = app.university
        app_data['status'] = app.status
        app_data['apply_date'] = app.apply_date.strftime('%Y-%m-%d %H:%M:%S')
        output.append(app_data)
    return jsonify({'applications': output})

# 创建新申请接口
@app.route('/api/applications', methods=['POST'])
@token_required
def create_application(current_user):
    data = request.get_json()
    new_app = Application(
        student_name=data.get('student_name'),
        university=data.get('university'),
        status=data.get('status')
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({'message': 'Application created successfully'})

# 更新申请状态接口
@app.route('/api/applications/<int:app_id>', methods=['PUT'])
@token_required
def update_application(current_user, app_id):
    app = Application.query.get(app_id)
    if not app:
        return jsonify({'message': 'Application not found'}), 404
    data = request.get_json()
    app.status = data.get('status', app.status)
    db.session.commit()
    return jsonify({'message': 'Application updated successfully'})

# 删除申请接口
@app.route('/api/applications/<int:app_id>', methods=['DELETE'])
@token_required
def delete_application(current_user, app_id):
    app = Application.query.get(app_id)
    if not app:
        return jsonify({'message': 'Application not found'}), 404
    db.session.delete(app)
    db.session.commit()
    return jsonify({'message': 'Application deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)