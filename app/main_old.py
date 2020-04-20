import json
import logging
import requests
import time
import urllib
import utils

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Flask, Blueprint
from flask_restplus import Resource, Api, fields
from usertable import UserTable

app = Flask(__name__)
#api = Api(app)

blueprint = Blueprint('api', __name__, url_prefix='')
api = Api(blueprint, 
        version='1.0', 
        title=' APIs for smishing', 
        description='Smishing 등록,수정,삭제,조회 API입니다',
        doc='/api/doc/'
        )
app.register_blueprint(blueprint)

#
# Name space for APIs
#
ns  = api.namespace('api/v1', 
        description='/User 사용자 등록,수정,삭제,조회'
        ) # /user 네임스페이스를 만든다


#
# List pagination for users.
#
resource_user = api.model('User', {
    'id': fields.Integer(description='user id'),
    'useremail': fields.String(description='The user email', required=True),
    'username': fields.String(description='The user name', required=True),
    'userphone': fields.String(description='The user phone', required=True),
    'userdesc': fields.String(description='user description or profile', required=False),
    'views': fields.Integer(min=0),        
})

resource_users = api.model('Users', {
    'users': fields.List(fields.Nested(resource_user), description='The user list'),
    'count': fields.Integer(min=0),
    'page': fields.Integer(min=0)
})


luParser = api.parser()
luParser.add_argument('page', type=int, help='Page number', location='query')
luParser.add_argument('itemsInPage', type=int, help='Number of Items in a page', location='query')


@ns.route('/users')
class Users(Resource):

    @api.expect(luParser)
    #@api.marshal_with(resource_users, as_list=False)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def get(self):
        ''' 사용자 정보를 리스트로 보여주며 페이지기능을 제공한다 '''
        return list_users()

#
# Post user data (user creation).
#
@ns.route('/user')
class UserAdd(Resource):

    @api.expect(resource_user, validate=False)
    @api.response(200, 'Success')
    def post(self):
        ''' 사용자 정보를 등록한다. '''
        return add_user()

#
# Managing user data (for retrieve, update, delete).
#
@ns.route('/user/<id>')
@api.doc(params={'id':'This is a userId or 사용자ID입니다.'})
class User(Resource):

    @api.marshal_with(resource_user, as_list=False)
    @api.response(200, 'Success')
    def get(self, id):
        ''' 사용자 정보의 상세내역을 조회한다. '''
        return get_user(id)

    @api.response(200, 'Success')
    @api.expect(resource_user, validate=False)    
    def put(self, id):
        ''' 사용자 정보를 변경한다. '''
        return update_user(id)

    @api.response(200, 'Success')
    def delete(self, id):
        ''' 사용자 정보를 삭제한다. '''
        return delete_user(id)


# INSERT 함수 예제
#@app.route('/user', methods=['POST'])
def add_user():

    j = request.get_json()

    print("DEBUG> input ===>{}".format(j))

    db = UserTable()
    result = db.insert(j)
    result = {"message":"ok"} if result is None else result

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

    return response


# LIST 예제
#@app.route('/users', methods=['GET'])
def list_users():

    page = int(request.args.get('page', "0"))
    np = int(request.args.get('itemsInPage', "20"))

    db = UserTable()
    res = db.list(page=page, itemsInPage=np)

    result = {
        "users" : "{}".format(res),
        "count" : len(res),
        "page"  : page
    }

    print("DEBUG> {}".format(result))
    return result


# Manage a user from users by ID 예제
#@app.route('/user/<id>', methods=['GET','PUT','DELETE'])
def manage_user(id):
    if request.method == 'GET':
        result = get_user(id)
    elif request.method == 'PUT':
        result = update_user(id)
    elif request.method == 'DELETE':
        result = delete_user(id)
    else:
        result = {
            "error" : "http method not found = {}".format(request.method)
        }

    return result;


# Get a user from users by ID 예제
def get_user(id):

    db = UserTable()
    result = db.get(id)

    return result


def update_user(id):

    j = request.get_json()
    db = UserTable()
    result = db.update(id,j)
    result = {"message":"ok"} if result is None else result

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

    return response


def delete_user(id):

    db = UserTable()
    result = db.delete(id)
    result = {"message":"ok"} if result is None else result

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
