# Time Series Forecaster

## MLFlow Server

Using this command to run the MLFlow Server:

```bash
mlflow server \
    --backend-store-uri sqlite:///notebooks/mlflow.sqlite \
    --default-artifact-root ./notebooks.mlruns 
```

## REST API

1. install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

2. change the directory to `time_series_forecaster`:

    ```bash
    cd time_series_forecaster
    ```

3. run the API:

    ```bash
    python manage.py runserver 
    ```

### Request

The API accepts a GET request to `/api/forecast` with the following example parameters:

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
        },
        {
            "time": "2019-01-01T00:00:03Z",
            "value": 2.0
        },
        {
            "time": "2019-01-01T00:00:04Z",
            "value": 3.0
        }
    ]
}
```

The Number of values for each dataset is specified in `mlruns.sqlite`, which chan be accessed through the mlfow server.

when the number of values sent in the request is less than the number of values specified in the dataset info, Bad Response is returned, with a declaration of the number of values needed.

### Response

The API returns a JSON response with the following format:

```json
{
   "prediction": "0.999",
   "timestamp": "2019-01-01T00:00:05Z"
}
```
