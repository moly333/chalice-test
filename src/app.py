from chalice import Chalice
import json
import boto3
from botocore.exceptions import ClientError
from chalice import NotFoundError


app = Chalice(app_name='chalice-test')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/view/{name}')
def view_prof(name):
    return {'name': name}


@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()


S3 = boto3.client('s3', 'ap-northeast-1')
BUCKET = 'chalice-test-objects'


@app.route('/objects/{key}', methods=['GET', 'PUT'])
def s3objects(key):
    request = app.current_request
    if request.method == 'PUT':
        S3.put_object(Bucket=BUCKET, Key=key,
                      Body=json.dumps(request.json_body))
    elif request.method == 'GET':
        try:
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
