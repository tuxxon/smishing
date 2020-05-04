from flask import Blueprint
from flask_restplus import Api

from .auth_controller import api as ns1
from .user_controller import api as ns2
from .upload_controller import api as ns3

#from .xclass_controller import api as nsx

blueprint = Blueprint('api', __name__, url_prefix='')
api = Api(blueprint,
    title='Smishing',
    version='0.1',
    description='APIs for smishing',
    doc='/api/doc/',
    # All API metadatas
)

api.add_namespace(ns1, path='/api/v1')
api.add_namespace(ns2, path='/api/v1')
api.add_namespace(ns3, path='/api/v1')