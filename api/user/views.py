from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.models import User, UserProfile
from api.permissions import IsOwnerOrReadOnly
from api.user.serializers import (UserFKSerializer, UserLoginSerializer,
                                  UserSerializer, UserUpdateSerializer)

from .serializers import UserRegistrationSerializer


class AuthCheck(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response({'message': 'pass'}, status=status.HTTP_200_OK)


class UserList(RetrieveAPIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserFKSerializer(users, many=True)
        return Response(serializer.data)


class UserListAny(RetrieveAPIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserFKSerializer(user)
        self.check_object_permissions(self.request, {'user': user.email})
        return Response(serializer.data)


class UserUpdate(UpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserUpdateSerializer

    def put(self, request, user_id):
        user = User.objects.get(pk=user_id)
        profile = UserProfile.objects.get(user_id=user_id)
        profileSerializer = UserSerializer(
            profile, data={'first_name': request.data.get('profile').get('first_name'),
                           'last_name': request.data.get('profile').get('last_name'), 'phone_number': request.data.get('profile').get('phone_number'),
                           'age': request.data.get('profile').get('age'), 'gender': request.data.get('profile').get('gender')}, partial=True)
        profileSerializer.is_valid(raise_exception=True)
        profileSerializer.save()
        if request.data.get('password'):
            serializer = self.serializer_class(
                user, data={'email': request.data.get('email'), 'password': request.data.get('password')}, partial=True)
        else:
            serializer = self.serializer_class(
                user, data={'email': request.data.get('email')}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Updated Successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)


class UserDelete(DestroyAPIView):
    permission_classes = (IsAdminUser,)

    def delete(self, _, user_id):
        user = User.objects.get(pk=user_id)
        user.delete()
        return Response({'success': 'Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)


class UserRegistrationView(CreateAPIView):

    permission_classes = (IsAdminUser,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered successfully!'
        }

        return Response(response, status=status_code)


class UserLoginView(RetrieveAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in successfully!',
            'token': serializer.data['token']
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


# User Profile View
class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'User profile fetched successfully!',
                'data': [
                    {
                        'first_name': user_profile.first_name,
                        'last_name': user_profile.last_name,
                        'phone_number': user_profile.phone_number,
                        'age': user_profile.age,
                        'gender': user_profile.gender
                    }
                ]
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'False',
                'status code': status_code,
                'message': 'User does not exists!',
                'error': str(e)
            }
        return Response(response, status=status_code)
