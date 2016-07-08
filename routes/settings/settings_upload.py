import configparser
import werkzeug
from flask_restful import Resource, reqparse
from routes.utils import makeResponse

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')


class UploadUsersFile(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        args['file'].save("%s" % config['importer']['json_users_path'])
        return makeResponse(True, 200)

    def options(self):
        return makeResponse(True, 200)


class UploadPostsFile(Resource):
    def post(self):
        # todo
        return makeResponse(True, 200)


class UploadCommentsFile(Resource):
    def post(self):
        # todo
        return makeResponse(True, 200)