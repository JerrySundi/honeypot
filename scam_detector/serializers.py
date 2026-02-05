from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=50)
    text = serializers.CharField()
    timestamp = serializers.CharField()


class MetadataSerializer(serializers.Serializer):
    channel = serializers.CharField(max_length=50, required=False)
    language = serializers.CharField(max_length=50, required=False)
    locale = serializers.CharField(max_length=10, required=False)


class HoneypotRequestSerializer(serializers.Serializer):
    sessionId = serializers.CharField(max_length=100)
    message = MessageSerializer()
    conversationHistory = serializers.ListField(
        child=MessageSerializer(),
        required=False,
        default=list
    )
    metadata = MetadataSerializer(required=False)


class HoneypotResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=20)
    reply = serializers.CharField()
