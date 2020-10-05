from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.GetAll.as_view()),
    path('post/', views.PostAll.as_view()),
    path('put/<uuid:intro_id>/', views.PutAny.as_view()),
    path('delete/<uuid:intro_id>/', views.DeleteAny.as_view())
]