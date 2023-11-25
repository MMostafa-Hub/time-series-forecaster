# Time Series Forecaster

## Running the API

1. build the docker image:

    ```bash
    docker build -t time-series-forecaster .
    ```

2. run the docker image:

    ```bash
    docker run -p 8000:8000 time-series-forecaster -d
    ```

## Rest API

After running the docker image, you can access the API at `http://localhost:8000`. or the port you specified in the `docker run` command.

### Request

The API accepts a GET request to `/forecast` with the following example parameters:

```json
{
    "dataset_id": "train_9",
    "values": [
        {
            "time": "2019-01-01T00:00:00Z",
            "value": 1.0
        },
        {
            "time": "2019-01-01T00:00:01Z",
            "value": 2.0
        },
        {
            "time": "2019-01-01T00:00:02Z",
            "value": 3.0
        }
    ]
}
```

The Number of values for each dataset is specified in `/data/dataset_info.json`, when the number of values sent in the request is less than the number of values specified in the dataset info, Bad Response is returned, with a declaration of the number of values needed.

### Response

The API returns a JSON response with the following format:

```json
{
   "prediction": "0.999"
}
```
