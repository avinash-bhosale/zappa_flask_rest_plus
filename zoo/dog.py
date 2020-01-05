from flask_restplus import Namespace, Resource, fields
import uuid
from boto3 import resource
dynamodb = resource('dynamodb')
dog_table = dynamodb.Table('dogs')

api = Namespace('dogs', description='Dogs related operations')

dog = api.model('Dog', {
    'id': fields.String(required=True),
    'name': fields.String(required=True, min_length=5, max_length=50),
    'description': fields.String(required=True, min_length=10, max_length=200)
})
new_dog = api.model('NewDog', {
    'name': fields.String(required=True, min_length=5, max_length=50),
    'description': fields.String(required=True, min_length=10, max_length=200)
})
dog_response = api.model('DogResponse', {
    'data': fields.Nested(dog),
    'status': fields.String(default="Success"),
    'statusCode': fields.String(default=200),
    'message': fields.String(default='Dog Info returned')
})
dog_list = api.model('DogResponseList', {
    'data': fields.List(fields.Nested(dog)),
    'status': fields.String(default="Success"),
    'statusCode': fields.String(default=200),
    'message': fields.String(default='Dog List returned')
})
DOGS = [
    {'id': 'medor', 'name': 'Medor', "description": "this is a dog"},
]


@api.route('/')
class DogList(Resource):
    @api.doc('list_dogs')
    @api.response(200, 'Dog List Returned', model=dog_list)
    @api.marshal_list_with(dog_list, code=200)
    @api.response(404, 'Dogs not found')
    def get(self):
        """List all dogs"""
        dogs_data = dog_table.scan()
        response = dict()
        if dogs_data.get('Items'):
            response["data"] = dogs_data['Items']
            return response
        api.abort(404, "Dogs Not found", status="False", statusCode=404)

    @api.doc('new_dog')
    @api.response(201, 'New Dog Created', model=dog_response)
    @api.expect(new_dog, validate=True)
    def post(self):
        payload = api.payload
        # payload
        dog_id = str(uuid.uuid4())
        dog_table.put_item(
            Item={
                'id': dog_id,
                'name': payload['name'],
                'description': payload['description'],
            }
        )
        dog_obj = dog_table.get_item(Key={'id': dog_id})
        return {
            'statusCode': 201,
            'message': 'Dog added successfully',
            'data': dog_obj['Item']
        }


@api.route('/<id>')
@api.param('id', 'The dog identifier')
@api.response(404, 'Dog not found')
class Dog(Resource):
    @api.doc('get_dog')
    @api.response(200, 'Dog Information Returned', model=dog_response)
    @api.marshal_with(dog_response, code=200)
    def get(self, id):
        """Find Dog by Dog ID"""
        dog_obj = dog_table.get_item(Key={'id': id})
        if dog_obj.get('Item'):
            return {'data': dog_obj['Item'], 'status': "Success", 'statusCode': 200}
        api.abort(404, "Dog Not found", status="False", statusCode=404)
