from flask import jsonify, request, render_template, make_response
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import (
    jwt_required, create_access_token,get_csrf_token, get_raw_jwt,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from werkzeug import secure_filename
from s3storage import S3Storage
from utils import hash_image

api = Namespace('Upload', description='the Apis for Upload')


@api.route('/upload/<id>')
class Upload(Resource):

    @jwt_required
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.produces(["text/html"])
    def get(self, id):
        ''' 업로드할 화면을 보여준다.'''

        headers = {'Content-Type' : 'text/html'}
        resp = make_response(
            render_template('upload.html',
                userId = id,
                csrf_token = get_raw_jwt().get('csrf')
                ),
            200,
            headers
            )

        return resp

    @jwt_required
    def post(self, id):
        ''' 실제로 업로드를 실행한다. '''

        f = request.files['imageFile']
        #f.save(secure_filename(f.filename))

        s = S3Storage()
        s.uploadTo("cf.stackcraft.co", id, f.filename, f)

        print("[DEBUG] ===> {}".format(f.filename))
        h = hash_image(f)
        print("[DEBUG] ===> {}".format(h))

        return jsonify({"msg":"Success", "imageUrl": s.getUrl(),"hash": h})