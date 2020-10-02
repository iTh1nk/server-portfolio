from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models
from api.pagination import CustomPagination

from . import serializers


class GetAll(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        project = models.Project.objects.all().order_by('-created_at')
        serializer = serializers.ProjectSerializer(project, many=True)
        return Response(serializer.data)


class GetAny(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, project_id):
        project = models.Project.objects.get(id=project_id)
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data)


class GetPage(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        project = models.Project.objects.all().order_by('-created_at')
        page = self.paginate_queryset(project)

        if page is not None:
            serializer = serializers.ProjectSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = serializers.ProjectSerializer(
                project, many=True)
            data = serializer.data

        return Response(data)


class PostAll(APIView):
    permission_classes = (IsAdminUser,)

    def project(self, request):
        print(request.data)
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Project Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PutAny(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, project_id):
        project = models.Project.objects.get(id=project_id)
        serializer = serializers.ProjectSerializer(project, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Updated Successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAny(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, _, project_id):
        project = models.Project.objects.get(id=project_id)
        project.delete()
        return Response({'success': 'Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
