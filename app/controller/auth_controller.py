from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from usertable import UserTable
from .user_controller import resource_user
from .user_controller import add_user


api = Namespace('Auth', description='the Apis for Auth')

resource_auth = api.model('Auth', {
    'id': fields.Integer(description='The user email', required=False),
    'useremail': fields.String(description='The user email', required=False),
    'userpass': fields.String(description='The user password', required=True)
})


uaParser = api.parser()
uaParser.add_argument('userpass', type=str, help='user password', location='query')


@api.route('/signin/<email>')
class Signin(Resource):

    @api.expect(uaParser)
    @api.response(200, 'Success')
    def get(self, email):
        ''' 사용자 인증정보를 인증한다. '''
        userpass = request.args.get('userpass')
        return get_auth(email,userpass)

    @api.expect(resource_auth)
    @api.response(200, 'Success')
    def post(self, email):
        ''' 사용자 인증정보를 인증한다. '''
        j = request.get_json()
        return get_auth(email, j.get('userpass'))


@api.route('/signup')
class Signup(Resource):

    #@api.expect(resource_user, validate=False)
    @api.response(200, 'Success')
    def post(self):
        ''' 사용자 인증정보를 등록한다. '''
        return add_user()

# Get a user from users by ID 예제
def get_auth(email,passwd):

    db = UserTable()
    result = db.auth(email, passwd)

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)


    # Set the JWT cookies in the response
    resp = jsonify({'login': result})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp

