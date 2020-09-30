from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserRegistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('get/', views.UserList.as_view()),
    path('get/<uuid:user_id>/', views.UserListAny.as_view()),
    path('put/<uuid:user_id>/', views.UserUpdate.as_view()),
    path('delete/<uuid:user_id>/', views.UserDelete.as_view()),
    path('check/', views.AuthCheck.as_view()),
]
