from rest_framework import serializers
from .models import Forecast, Value, Dataset


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ["value", "time"]


class ForecastSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True)

    class Meta:
        model = Forecast
        fields = ["dataset_id", "values"]

    def validate_values(self, values):
        pipeline = Dataset.objects.get(
            dataset_id=self.initial_data["dataset_id"]
        ).get_pipeline()

        max_lag = max(pipeline["autocorrelation"].significant_lags)
        if len(values) < max_lag:
            raise serializers.ValidationError(
                f"The minimum number of values is {max_lag}"
            )
        return values

    def create(self, validated_data):
        values_data = validated_data.pop("values")
        forecast = Forecast.objects.create(**validated_data)
        for value_data in values_data:
            Value.objects.create(forecast=forecast, **value_data)
        return forecast
