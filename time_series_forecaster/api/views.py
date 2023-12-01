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

        dataset_id = request_body["dataset_id"]
        client = MLFlowExperiment(dataset_id)

        # Load the preprocessing pipeline and the model
        model = client.get_model()
        pipeline = client.get_pipeline()

        # Load the params
        params = client.get_run_params()

        interval = pd.Timedelta(params["index_interval"])
        max_lags = int(params["max_lags"])

        # Check if the request body has the required values
        if len(request_body["values"]) < max_lags:
            return JsonResponse(
                {
                    "error": f"Please provide at least {max_lags} values to make a prediction."
                },
                status=400,
            )

        # Transform the input to a dataframe
        transformed_input = self.__get_test_input(request_body["values"], interval)

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
        self, values: List[dict], interval: pd.Timedelta
    ) -> pd.DataFrame:
        transformed_input = self.__input_to_dataframe(values)

        # add a new record with the last time index + interval
        last_time_index = transformed_input.index[-1]
        new_time_index = last_time_index + interval

        transformed_input.loc[new_time_index] = np.nan

        return transformed_input

    def __input_to_dataframe(self, values: List[dict]) -> pd.DataFrame:
        time_index_list = []
        value_list = []
        for value in values:
            value_list.append(value["value"])
            time_index_list.append(value["time"])

        # Change the type of the time index to datetime
        time_index_list = pd.to_datetime(time_index_list)
        return pd.DataFrame({"value": value_list}, index=time_index_list)
