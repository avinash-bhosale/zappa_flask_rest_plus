from flask_restplus import Namespace, Resource, fields

api = Namespace('dogs', description='Dogs related operations')

dog = api.model('Dog', {
    'id': fields.String(required=True, description='The dog identifier'),
    'name': fields.String(required=True, description='The dog name'),
    'description': fields.String(required=True, min_length=5, max_length=200, description='The Dog Description')
})
new_dog = api.model('NewDog', {
    'name': fields.String(required=True, description='The dog name'),
    'description': fields.String(required=True, min_length=5, max_length=200, description='The Dog Description')
})
DOGS = [
    {'id': 'medor', 'name': 'Medor', "description": "this is a dog"},
]


@api.route('/')
class DogList(Resource):
    @api.doc('list_dogs')
    @api.marshal_list_with(dog)
    def get(self):
        """List all dogs"""
        return DOGS

    @api.doc('list_dogs')
    @api.expect(new_dog, validate=True)
    def post(self):
        return {'message': "this is what we do"}


@api.route('/<id>')
@api.param('id', 'The dog identifier')
@api.response(404, 'Dog not found')
class Dog(Resource):
    @api.doc('get_dog')
    @api.marshal_with(dog)
    def get(self, id):
        '''Fetch a dog given its identifier'''
        for dog in DOGS:
            if dog['id'] == id:
                return dog
        api.abort(404)
