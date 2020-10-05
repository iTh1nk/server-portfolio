from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models

from . import serializers


class GetAll(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        intro = models.Intro.objects.all().order_by('-created_at')
        serializer = serializers.IntroSerializer(intro, many=True)
        return Response(serializer.data)


class PostAll(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.IntroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Post Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PutAny(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, intro_id):
        intro = models.Intro.objects.get(id=intro_id)
        serializer = serializers.IntroSerializer(intro, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Updated Successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAny(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, _, intro_id):
        intro = models.Intro.objects.get(id=intro_id)
        # if intro.is_valid():
        #     intro.delete()
        #     return Response({'success': 'Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
