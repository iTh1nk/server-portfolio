from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.GetAll.as_view()),
    path('get/<uuid:message_id>/', views.GetAny.as_view()),
    path('get/page/', views.GetPage.as_view()),
    path('post/', views.PostAll.as_view()),
    path('delete/<uuid:message_id>/', views.DeleteAny.as_view())
]
