import json
import os
import random
from datetime import datetime, timezone

import boto3

sns = boto3.client('sns')
TOPIC_ARN = os.environ['TOPIC_ARN']

def publicar_lectura(sensor_id, medicion, unidad_medida):
    tenant_id = 'FAB1'
    fecha_hora = datetime.now(timezone.utc).isoformat(timespec='microseconds')

    lectura = {
        'tenant_id': tenant_id,
        'sensor_id': sensor_id,
        'lectura_id': f'{sensor_id}.{fecha_hora}',
        'lectura_datos': {
            'medicion': medicion,
            'unidad_medida': unidad_medida
        }
    }

    respuesta = sns.publish(
        TopicArn=TOPIC_ARN,
        Subject='Nueva Lectura Sensor',
        Message=json.dumps(lectura),
        MessageAttributes={
            'tenant_id': {
                'DataType': 'String',
                'StringValue': tenant_id
            },
            'sensor_id': {
                'DataType': 'String',
                'StringValue': sensor_id
            },
            'medicion': {
                'DataType': 'Number',
                'StringValue': str(medicion)
            }
        }
    )

    print(json.dumps({
        'lectura': lectura,
        'message_id': respuesta['MessageId']
    }))
    return lectura

def lambda_handler(event, context):
    co2 = publicar_lectura(
        sensor_id='CO2',
        medicion=random.randint(400, 1000),
        unidad_medida='PPM'
    )

    temperatura = publicar_lectura(
        sensor_id='TEMP',
        medicion=random.randint(10, 60),
        unidad_medida='CELSIUS'
    )

    return {
        'statusCode': 200,
        'lecturas_publicadas': [co2, temperatura]
    }
