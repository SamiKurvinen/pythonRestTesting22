from flask_restful import Resource, reqparse
from models.user import UserModel

class userRegister(Resource):
    """
    This res allows users to register via POST method (user & pass)
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This cannot be blank')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This cannot be blank')

    def post(self):
        data = userRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already in use'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully'}, 201