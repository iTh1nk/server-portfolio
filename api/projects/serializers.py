from rest_framework import serializers

from api.models import Project

from api import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"
