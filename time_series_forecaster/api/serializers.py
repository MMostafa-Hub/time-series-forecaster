from rest_framework import serializers
from .models import Forecast, Dataset

class ValueSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    value = serializers.FloatField()

class ForecastSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True)

    class Meta:
        model = Forecast
        fields = ['dataset_id', 'values']

    def validate(self, attrs):
        self.validate_dataset_id(attrs['dataset_id'])
        self.validate_values(attrs['values'])
        return super().validate(attrs)
    
    def validate_dataset_id(self, dataset_id):
        try:
            dataset = Dataset.objects.get(dataset_id=dataset_id)
        except Dataset.DoesNotExist:
            raise serializers.ValidationError("Invalid dataset_id")
        return dataset_id

    def validate_values(self, values):
        if len(values) < 5:
            raise serializers.ValidationError("The minimum number of values is 5")
        return values

    def create(self, validated_data):
        values_data = validated_data.pop('values')
        forecast = Forecast.objects.create(**validated_data)
        for value_data in values_data:
            forecast.values.create(**value_data)
        return forecast
