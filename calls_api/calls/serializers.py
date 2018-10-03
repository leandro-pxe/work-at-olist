from rest_framework import serializers
from .models import CallRecord


class CallRecordSerializer(serializers.Serializer):
    type = serializers.CharField()
    date_register = serializers.DateTimeField()
    call_id = serializers.CharField()
    source = serializers.CharField()
    destination = serializers.CharField()

    def create(self, validated_data):
        return CallRecord.objects.create(**validated_data)

    def validate_source(self, value):
        if len(value) not in [10, 11] or not value.isdigit():
            raise serializers.ValidationError("Source phone has 10 or 11 digits with code area")
        return value

    def validate_destination(self, value):
        if len(value) not in [10, 11] or not value.isdigit():
            raise serializers.ValidationError("Destination phone hasn't 10 or 11 digits with code area")
        return value

    def validate_type(self, value):
        if value not in ['START', 'END']:
            raise serializers.ValidationError("Type has to be START or END.")
        return value

    def validate_call_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Call ID has to be numeric.")
        return value


class BillSerializer(serializers.Serializer):
    destination = serializers.CharField()
    call_start_date = serializers.DateField()
    call_start_time = serializers.TimeField()
    call_duration = serializers.TimeField()
    call_price = serializers.CharField()

