import json
import boto3

table = boto3.resource('dynamodb').Table('t_sensor_iot_FAB1')

def lambda_handler(event, context):
    for record in event['Records']:
        sobre_sns = json.loads(record['body'])
        lectura = json.loads(sobre_sns['Message'])

        table.put_item(Item=lectura)
        print('Lectura registrada:', json.dumps(lectura))

    return {
        'statusCode': 200,
        'cantidad_registrada': len(event['Records'])
    }
