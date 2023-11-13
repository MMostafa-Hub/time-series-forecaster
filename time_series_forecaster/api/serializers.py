from rest_framework import serializers
from .models import Forecast, Value


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ["value", "time"]


class ForecastSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True)

    class Meta:
        model = Forecast
        fields = ["dataset_id", "values"]

    def validate(self, attrs):
        super().validate(attrs)
        self.validate_values(attrs.get("values"))
        return attrs

    def validate_values(self, values):
        if len(values) < 5:
            raise serializers.ValidationError("The minimum number of values is 5")
        return values

    def create(self, validated_data):
        values_data = validated_data.pop("values")
        forecast = Forecast.objects.create(**validated_data)
        for value_data in values_data:
            Value.objects.create(forecast=forecast, **value_data)
        return forecast
