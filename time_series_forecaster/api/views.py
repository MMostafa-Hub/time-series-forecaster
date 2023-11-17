from datetime import datetime
import numpy as np
from rest_framework.response import Response
from .serializers import ForecastSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from .models import Dataset, Forecast
import pandas as pd
from typing import List


class ForecastView(APIView):
    def get(self, request) -> Response:
        forecast_serializer = ForecastSerializer(data=request.data)

        if not forecast_serializer.is_valid(raise_exception=True):
            return JsonResponse({"error": forecast_serializer.errors}, status=400)

        forecast_serializer.save()

        dataset = Dataset.objects.get(dataset_id=request.data["dataset_id"])

        # Load the preprocessing pipeline and the model
        model = dataset.get_model()
        preprocessing_pipeline = dataset.get_pipeline()

        # Transform the input to the format expected by the model
        transformed_input = self.__get_test_input(
            forecast_serializer.data["values"], dataset
        )
        pre_transformed_input = preprocessing_pipeline.transform(transformed_input)
        input_to_model = (
            pre_transformed_input.iloc[-1, :].drop("value").values.reshape(1, -1)
        )

        return JsonResponse(
            {"prediction": model.predict(input_to_model)[0]}, status=status.HTTP_200_OK
        )

    def __get_test_input(self, values: List[dict], dataset: Dataset) -> pd.DataFrame:
        transformed_input = self.__input_to_dataframe(values)

        # add a new record with the last time index + interval
        last_time_index = transformed_input.index[-1]
        new_time_index = last_time_index + dataset.interval

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
