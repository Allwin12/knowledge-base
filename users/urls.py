from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserView.as_view(), name='user'),
    path('token/', views.TokenView.as_view(), name='access-token')
]
