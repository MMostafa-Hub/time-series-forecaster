from .mlflow_experiment import MLFlowExperiment
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from typing import List
import pandas as pd
import numpy as np


class ForecastView(APIView):
    def get(self, request) -> Response:
        request_body = request.data

        # Get the request parameters
        dataset_id = "train_" + request_body["dataset_id"]
        start_timestamp = pd.to_datetime(request_body["start_timestamp"])
        test_dataset_path = request_body["test_dataset_path"]
        test_dataset = pd.read_csv(test_dataset_path, index_col=0, parse_dates=True)

        client = MLFlowExperiment(dataset_id)

        # Load the preprocessing pipeline and the model
        model = client.get_model()
        pipeline = client.get_pipeline()

        # Load the params
        params = client.get_run_params()

        interval = pd.Timedelta(params["index_interval"])
        max_lags = int(params["max_lags"])

        # Transform the input to a dataframe
        transformed_input = self.__get_test_input(
            test_dataset, start_timestamp, max_lags, interval
        )

        # Transform the input to the format expected by the model
        pre_transformed_input = pipeline.transform(transformed_input)
        input_to_model = (
            pre_transformed_input.iloc[-1, :].drop("value").values.reshape(1, -1)
        )

        # Create an inference json response
        prediction = model.predict(input_to_model)[0]
        timestamp = transformed_input.index[-1] + interval

        response = {
            "prediction": prediction,
            "timestamp": timestamp,
        }

        return JsonResponse(response, status=status.HTTP_200_OK)

    def __get_test_input(
        self,
        test_dataset: pd.DataFrame,
        start_timestamp: pd.DatetimeIndex,
        max_lags: int,
        interval: pd.Timedelta,
    ) -> pd.DataFrame:
        # Search for the start_timestamp in the test dataset
        if start_timestamp not in test_dataset.index:
            raise ValueError("The start_timestamp is not in the test dataset.")
        
        test = test_dataset.loc[start_timestamp:]

        # Take the first max_lags rows
        if len(test) < max_lags:
            raise ValueError("Not enough data to make a prediction.")

        transformed_input = test.iloc[:max_lags, :]
        
        
        # add a new record with the last time index + interval
        last_time_index = transformed_input.index[-1]
        new_time_index = last_time_index + interval
        
        transformed_input.loc[new_time_index] = np.nan
        return transformed_input
