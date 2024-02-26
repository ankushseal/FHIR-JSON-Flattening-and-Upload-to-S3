**README**

## FHIR JSON Flattening and Upload to S3

This repository contains a Python script for fetching FHIR JSON data from an API, flattening it, and uploading the flattened data to an Amazon S3 bucket.

### Prerequisites

Before running the script, ensure you have the following dependencies installed:

- Python 3.x
- `requests`
- `boto3`

You can install the dependencies via pip:

```bash
pip install requests boto3
```

### Configuration

Make sure to update the following information in the script:

- `config.json`: Provide your AWS credentials (AWS Access Key ID and AWS Secret Access Key).
- `api_url`: URL of the API endpoint from which to fetch FHIR JSON data.
- `bucket_name`: Name of the S3 bucket where the flattened data will be uploaded.
- `polling_interval`: Interval (in seconds) for polling the API and uploading data to S3.

### Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/fhir-json-flattening.git
cd fhir-json-flattening
```

2. Update the `config.json` file with your AWS credentials.

3. Run the Python script `main.py`:

```bash
python main.py
```

### Description

This script periodically fetches FHIR JSON data from the specified API endpoint, flattens it, and uploads the flattened data to an Amazon S3 bucket. It follows a polling mechanism with a specified interval to ensure regular updates.

### Input

- FHIR JSON data fetched from the API specified in `api_url`.

### Output

- Flattened FHIR JSON data uploaded to the specified S3 bucket.
- Logs indicating the status of data retrieval, flattening, and uploading.

### Contributing

Contributions are welcome! If you have suggestions, feature requests, or bug fixes, please feel free to open an issue or create a pull request.

### Acknowledgements

- [requests](https://docs.python-requests.org/en/master/) - HTTP library for Python.
- [boto3](https://github.com/boto/boto3) - AWS SDK for Python.

### Workflow

### Step 1:

I have created a local JSON server, which is available as a NPM package. By running “ npm install -g json-server ” command, we can install the server in our local machine.
Then we need to create a JSON file. Here I have taken a dummy FHIR JSON data as ‘db.json’ .
After that we need to start the server with “ json-server --watch db.json “ this command.

Db.json :

![image](https://github.com/ankushseal/JsonServer_to_S3_Processing/assets/65338558/fd944d10-3e83-4945-aef5-19e4deeabd64)


Starting the server :

![image](https://github.com/ankushseal/JsonServer_to_S3_Processing/assets/65338558/a4769af9-71c7-40d4-94e7-e20c8137d67d)


Now we are ready with our Json server.

### Step 2 :

Now it’s time to test the server. To test the server I have used POSTMAN software.
Postman Interface :

![image](https://github.com/ankushseal/JsonServer_to_S3_Processing/assets/65338558/58c106db-3f1b-4bae-bb29-b70149fded6d)


Here we have many options. When I opt GET, I got the db.json’s data as output. There is another option like PUT by that we can put new Json in our server.

Reference : [Create A REST API With JSON Server | by Sebastian | CodingTheSmartWay | Medium](https://medium.com/codingthesmartway-com-blog/create-a-rest-api-with-json-server-36da8680136d)

Step 3 :

After creating and testing the server I build a python framework, which can read the Json data from our server. After successfully got the data it can upload the data in S3 bucket by creating a unique file name every time. After uploading the Json file, it will flatten the Json data and will upload the flatten data in another S3 bucket as txt file.
After doing all the process it will wait for 10 mins after that it’ll repeat the process again.


Output:

![image](https://github.com/ankushseal/JsonServer_to_S3_Processing/assets/65338558/d0f34a31-1f9e-4084-acdf-960be74d4371)

Json file in S3 bucket :

![image](https://github.com/ankushseal/JsonServer_to_S3_Processing/assets/65338558/ebd8343e-85f6-4b6a-9370-99b5a014279b)


Flatten Output in S3 Bucket:

![image](https://github.com/ankushseal/JsonServer_to_S3_Processing/assets/65338558/fdd1f15c-051e-407a-974b-1ecad3681c21)


Flattened object’s output :

![image](https://github.com/ankushseal/JsonServer_to_S3_Processing/assets/65338558/b9820ab5-33fd-4512-b9a7-dc888c5f52f4)


