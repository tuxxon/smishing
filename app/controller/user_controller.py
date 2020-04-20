from flask import jsonify
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies, get_raw_jwt,
    set_refresh_cookies, unset_jwt_cookies
)

from usertable import UserTable

api = Namespace('User', description='Apis for users')

#
# List pagination for users.
#
resource_user = api.model('User', {
    'id': fields.Integer(description='user id'),
    'useremail': fields.String(description='The user email', required=True),
    'userpass': fields.String(description='The user password', required=True),
    'username': fields.String(description='The user name', required=True),
    'userphone': fields.String(description='The user phone', required=True),
    'userdesc': fields.String(description='user description or profile', required=False),
    'token': fields.String(description='jwt token', required=False),    
    'views': fields.Integer(min=0),
})

luParser = api.parser()
luParser.add_argument('page', type=int, help='Page number', location='query')
luParser.add_argument('itemsInPage', type=int, help='Number of Items in a page', location='query')


@api.route('/users')
class Users(Resource):

    @api.expect(luParser)
    #@api.marshal_with(resource_users, as_list=True)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def get(self):
        ''' 사용자 정보를 리스트로 보여주며 페이지기능을 제공한다 '''
        return list_users()

#
# Post user data (user creation).
#

@api.route('/user')
class UserAdd(Resource):

    @api.expect(resource_user, validate=False)
    @api.response(200, 'Success')
    def post(self):
        ''' 사용자 정보를 등록한다. '''
        return add_user()

#
# Managing user data (for retrieve, update, delete).
#
@api.route('/user/<id>')
@api.doc(params={'id':'This is a userId or 사용자ID입니다.'})
class User(Resource):

    @jwt_required
    @api.response(200, 'Success')
    def get(self, id):
        ''' 사용자 정보의 상세내역을 조회한다. '''
        return get_user(id)

    @jwt_required
    @api.response(200, 'Success')
    @api.expect(resource_user, validate=False)
    def put(self, id):
        ''' 사용자 정보를 변경한다. '''
        return update_user(id)

    @jwt_required
    @api.response(200, 'Success')
    def delete(self, id):
        ''' 사용자 정보를 삭제한다. '''
        return delete_user(id)


# INSERT 함수 예제
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

# Get a user from users by ID 예제
def get_user(id):

    db = UserTable()
    result = db.get(id)
    result['token'] = get_raw_jwt()
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
