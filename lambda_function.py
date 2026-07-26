import json
import boto3
import uuid
import os

localstack_host = os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')
dynamodb = boto3.resource('dynamodb', endpoint_url=f'http://{localstack_host}:4566', region_name='us-east-1')
table = dynamodb.Table('Notes')

def handler(event, context):
    method = event.get('httpMethod', '')
    
    if method == 'POST':
        return create_note(event)
    elif method == 'GET':
        return read_note(event)
    elif method == 'PUT':
        return update_note(event)
    elif method == 'DELETE':
        return delete_note(event)
    else:
        return response(400, {'error': 'Unsupported method'})

def create_note(event):
    body = json.loads(event.get('body', '{}'))
    note_id = str(uuid.uuid4())
    table.put_item(Item={'id': note_id, 'content': body.get('content', '')})
    return response(201, {'id': note_id, 'message': 'Note created'})

def read_note(event):
    note_id = event.get('pathParameters', {}).get('id')
    result = table.get_item(Key={'id': note_id})
    item = result.get('Item')
    if not item:
        return response(404, {'error': 'Note not found'})
    return response(200, item)

def update_note(event):
    note_id = event.get('pathParameters', {}).get('id')
    body = json.loads(event.get('body', '{}'))
    table.update_item(
        Key={'id': note_id},
        UpdateExpression='SET content = :c',
        ExpressionAttributeValues={':c': body.get('content', '')}
    )
    return response(200, {'message': 'Note updated'})

def delete_note(event):
    note_id = event.get('pathParameters', {}).get('id')
    table.delete_item(Key={'id': note_id})
    return response(200, {'message': 'Note deleted'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
