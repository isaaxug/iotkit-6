import json
import boto3
from datetime import datetime

iot = boto3.client('iot-data')

def lambda_handler(event, context):
    topic = 'speaker/voice-kit/say'
    text = '現在の温度は、{}度です。'.format(_get_temp(event['sensors'][0]))
    payload = {
        'text': text
    }
    try:
        iot.publish(
            topic=topic,
            qos=0,
            payload=json.dumps(payload, ensure_ascii=False)
        )

        return {
            'statusCode': 200,
            'body': 'Succeeded.'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Failed.'
        }

def _get_temp(sensor):
    return round(int(sensor['temperature']))
