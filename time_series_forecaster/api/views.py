from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Forecast, Dataset
from .serializers import ForecastSerializer

class ForecastView(APIView):
    def get(self, request) -> Response:
        ForecastSerializer(data=request.data).validate(request.data)
    
        return Response(status=status.HTTP_200_OK)
