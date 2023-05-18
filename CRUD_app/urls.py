from rest_framework import routers
from django.urls import path, include
from .views import BoxUpdateViewSet, BoxListViewSet, BoxCreateViewSet, BoxDeleteViewSet


urlpatterns = [
    path('boxes/create', BoxCreateViewSet.as_view(), name='box-create'),
    path('boxes/<int:pk>/delete', BoxDeleteViewSet.as_view(), name='box-delete'),
    path('boxes/<int:pk>/update', BoxUpdateViewSet.as_view(), name='box-update'),
    path('boxes/list', BoxListViewSet.as_view(), name='box-list'),
]