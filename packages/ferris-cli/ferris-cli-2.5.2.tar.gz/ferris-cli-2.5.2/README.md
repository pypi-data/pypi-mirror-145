Ferris Cli
=====================
[![Downloads](https://pepy.tech/badge/ferris-cli)](https://pepy.tech/project/ferris-cli)

The following library simplifies the process of 
* forwarding Metrics and Task to a Kafka consumer.
* storing and retreiving application properties on the Ferris Platform
* setting up scheduler actions from within the Ferris Platform

SEE WIKI FOR MORE DETAILS

### Version 2 `ferris_cli.v2` is released!

### Usage

```python
from ferris_cli.v2 import ApplicationConfigurator, FerrisEvents, FerrisLogging
```
 

# Features

## Configuration

`ApplicationConfigurator` is used for fetching configuration from consul. 

```python
from ferris_cli.v2 import ApplicationConfigurator

config = ApplicationConfigurator().get(config_key="some.config.key")
```

`config_key` -> name of the Consul key to be retreived

If `config_key` is not provided value of env variable `APP_NAME` will be used instead of it and fetched configuration will be merged with `os.environ` dict. 


## Events

`FerrisEvents` class can be used for sending events in a standardized format that is used by all services. 

```python
from ferris_cli.v2 import FerrisEvents

FerrisEvents().send(
    event_type="some.event.type",
    event_source="some.event.source",
    data=dict(
        key_1="value_1",
        key_2="value_2"
    ),
    topic="events.topic",
    reference_id='somerefid'
)
```

| key        | required | description                             |
|------------|----------|-----------------------------------------|
| event_type | yes      | Type of the event that will be sent     |
| event_source | yes | Source of the event (e.g. service name) |
| data | yes | Dictionary with data that should be sent with event |
| topic | no | Name of the Kafka topic to which event will be sent. If not provided `DEFAULT_TOPIC` configuration value will be used. |
| reference_id | no | Custom value that can be sent with event and used for identification of chained events. |


## Minio handler

```python
from ferris_cli.v2.services.storage import MinioService

config = {
    "MINIO_HOST": "localhost",
    "MINIO_ACCESS_KEY": "someaccesskey",
    "MINIO_SECRET_KEY": "somesupersecretkey",
    "MINIO_SECURE_CONNECTION": False
}

minio_service = MinioService(config)

# retreive lis of all buckets
buckets = minio_service.get_buckets()

# retreive single bucket by name, if exists
bucket = minio_service.get_bucket_by_name(bucket_name="somebucket")

# create object in bucket
uploaded_file_name, file_hash = minio_service.create_object(file=fileobject, bucket_name="somebucket", supported_extensions=["txt", "json"])

# retreive list of all objects within bucket
minio_service.get_all_from_bucket(bucket_name="somebucket")

# retreive number of objects within bucket
minio_service.get_number_of_objects_in_bucket(bucket_name="somebucket")

# create bucket
minio_service.create_bucket(bucket_name="somebucket")

# delete bucket
minio_service.delete_bucket(bucket_name="somebucket")

# download object from bucket to local /tmp dir
minio_service.download_file(filename="nameofthefile.txt", bucket="somebucket")

# delete object from bucket
minio_service.delete_object(bucket_name="somebucket", object_name="someobjectname")

# copy object from one bucket to another
minio_service.copy_file(source_bucket="sourcebucketname", source_object="sourceobjectname", dest_bucket="destinationbucketname", dest_object="destinationobjectname")

# move object from one bucket to another
minio_service.move(source_bucket="sourcebucketname", source_object="sourceobjectname", dest_bucket="destinationbucketname", dest_object="destinationobjectname")
```

