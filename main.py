import json
import requests
import boto3
import datetime
import time

file=open("config.json")
config=json.load(file)
s3_client = boto3.resource(
            service_name="s3",
            region_name="us-east-1",
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config["aws_secret_access_key"]
        )
def fetch_json_from_api(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching data from API: {e}")
        return None

def upload_to_s3(json_data, bucket_name, object_name):
    try:
        object = s3_client.Object(bucket_name, object_name)
        object.put(Body=json.dumps(json_data))
        print(f"Successfully uploaded data to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Failed to upload data to S3: {e}")


def flatten_json(json_object, parent_key='', separator='.'):
    flat_dict = {}
    for k, v in json_object.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            flat_dict.update(flatten_json(v, new_key, separator=separator))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                list_key = f"{new_key}[{i}]"
                if isinstance(item, dict):
                    flat_dict.update(flatten_json(item, list_key, separator=separator))
                else:
                    flat_dict[list_key] = item
        else:
            flat_dict[new_key] = v
    return flat_dict


# Define function to read FHIR JSON file, flatten it, and write to a text file in S3
def read_and_write_fhir_json(input_filename,out_bucket_name,out_object_name):
    try:
        fs = {'patients': input_filename}
        sd=json.dumps(fs)
        #print(sd)
        fhir_data = json.loads(sd)
        #print(type(fhir_data))
        flattened_data = flatten_json(fhir_data)
        #print(flattened_data)
        op=""
        object = s3_client.Object(out_bucket_name, out_object_name)
        for key, value in flattened_data.items():
            op=op+(f"{key}: {value}\n")
        object.put(Body=op)
        return f"Flattened FHIR JSON data has been written to {out_object_name}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Replace with your API URL
    api_url = "http://localhost:3000/patients"

    # Replace with your S3 bucket name and object name
    bucket_name = "jsontest404"
    object_name = f"obj_ {datetime.datetime.now()}.json"

    # Polling interval in seconds (600 seconds = 10 minutes)
    polling_interval = 600

    while True:
        # Fetch JSON data from API
        json_data = fetch_json_from_api(api_url)
        print(json_data)

        if json_data:
            # Upload JSON data to S3
            upload_to_s3(json_data, bucket_name, object_name)
            #print("waiting for the json file to be created in s3 to continue the flatten process")
            #time.sleep(10)
            out_bucket_name = "jsontest404output"
            out_object_name = f"flattened_{object_name}.txt"
            #json_data = s3_client.Object(bucket_name, object_name).get()
            print(json_data)
            print(read_and_write_fhir_json(json_data,out_bucket_name,out_object_name))


        # Sleep for 10 minutes before the next polling cycle
        print(f"Sleeping for {polling_interval} seconds...")
        time.sleep(polling_interval)
