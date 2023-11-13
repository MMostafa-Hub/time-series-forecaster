from rest_framework.response import Response
from .serializers import ForecastSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from .models import Pipeline, Dataset
import pandas as pd
from typing import List


class ForecastView(APIView):
    def get(self, request) -> Response:
        forecast_serializer = ForecastSerializer(data=request.data)

        if not forecast_serializer.is_valid(raise_exception=True):
            return JsonResponse({"error": forecast_serializer.errors}, status=400)

        forecast_serializer.save()

        # Load the preprocessing pipeline and the model
        preprocessing_pipeline = Pipeline.objects.first().get_preprocessing_pipeline()
        model = Dataset.objects.get(dataset_id=request.data["dataset_id"]).get_model()

        # Convert the input data to a dataframe
        input = self.__input_to_dataframe(request.data["values"])
        return Response(status=status.HTTP_200_OK)

    def __input_to_dataframe(self, values: List[dict]) -> pd.DataFrame:
        time_index_list = []
        value_list = []
        for value in values:
            value_list.append(value["value"])
            time_index_list.append(value["time"])

        # Change the type of the time index to datetime
        time_index_list = pd.to_datetime(time_index_list)
        return pd.DataFrame({"value": value_list}, index=time_index_list)
