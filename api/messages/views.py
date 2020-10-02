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
        message = models.Message.objects.all().order_by('-created_at')
        serializer = serializers.MessageSerializer(message, many=True)
        return Response(serializer.data)


class GetAny(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, message_id):
        message = models.Message.objects.get(id=message_id)
        serializer = serializers.MessageSerializer(message)
        return Response(serializer.data)


class GetPage(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        message = models.Message.objects.all().order_by('-created_at')
        page = self.paginate_queryset(message)

        if page is not None:
            serializer = serializers.MessageSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = serializers.MessageSerializer(
                message, many=True)
            data = serializer.data

        return Response(data)


class PostAll(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = serializers.MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Message Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAny(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, _, message_id):
        message = models.Message.objects.get(id=message_id)
        message.delete()
        return Response({'success': 'Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
