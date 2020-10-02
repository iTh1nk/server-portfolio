from rest_framework import serializers

from api.models import Message

from api import models


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = "__all__"
