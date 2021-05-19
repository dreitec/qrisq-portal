from rest_framework import serializers


class SendMessageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    message = serializers.CharField()