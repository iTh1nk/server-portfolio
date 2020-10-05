from rest_framework import serializers

from api.models import Intro

from api import models


class IntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Intro
        fields = "__all__"
