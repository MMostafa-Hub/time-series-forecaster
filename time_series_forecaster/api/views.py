from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class ForecastView(APIView):
    def get(self, request) -> Response:
        return Response({"prediction": 0.5}, status=status.HTTP_200_OK)
