from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserModelSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    # pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
