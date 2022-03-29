from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, ListAPIView, \
    RetrieveUpdateAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.permissions import IsAdminOrIsSelf, IsOwnerOrReadOnly
from users.serializers import UserDetailSerializer, UserCreateSerializer, GradeSerializer, GradeCreateSerializer


class UserRetrieveDestroyViewSet(RetrieveDestroyAPIView,
                                 viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminOrIsSelf, ]


class UserListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer


class GradeCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = GradeCreateSerializer
    permissions = [IsOwnerOrReadOnly, IsAuthenticated, ]


class GradeUpdateRetrieve(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = GradeSerializer
    permissions = [IsOwnerOrReadOnly, IsAuthenticated, ]
