from rest_framework import serializers

from api.models import Post

from api import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = "__all__"
