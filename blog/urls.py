from django.urls import include
# from django.conf.urls import url
from rest_framework import routers
from . import views
from django.urls import include, re_path

router = routers.DefaultRouter()
 
 
urlpatterns = [
    re_path('login/', views.login),
    re_path('register/', views.register),
    re_path('transaction/', views.make_transaction),
    re_path('transaction_auth/', views.status_transaction_auth),
]