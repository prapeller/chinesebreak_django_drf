from django.shortcuts import render

from core.models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer