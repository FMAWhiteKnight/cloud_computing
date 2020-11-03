import json
from botocore.vendored import requests
import boto3

api_key = "d626743151bf083c5ea6c5f3a9a6e6d5"
s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    db_entry = dynamodb_client.get_item(
        TableName="global_count", 
        Key={ 
            'index': {'N': "0"}
            
        }
    )
    
    count = (db_entry["Item"]["file_count"]["N"])
    
    db_entry = dynamodb_client.update_item(
        TableName="global_count", 
        Key={ 
            'index': {'N': "0"}
        },
        UpdateExpression="SET file_count = file_count + :inc",
        ExpressionAttributeValues={
            ':inc': {"N": "1"},
        }

    )    
    
    city = (event["city"])
    # city = "boston"
    weather_response = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+",840&appid="+ api_key+ "&units=imperial").json()
    
    uploadByteStream = bytes(json.dumps(weather_response).encode('UTF-8'))
    
    
    filename = city + "_weather_" + count + ".txt"
    
    s3_client.put_object(Bucket='cloudcomputinghwgroupa', Key=filename, Body=uploadByteStream)
  