"""animeet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from shikimori.views import *

from users.views import UserRetrieveDestroyViewSet, UserCreateView, UserListView, GradeCreateView, \
    GradeUpdateRetrieve

router = routers.DefaultRouter()
router.register(r'api/v1/users', UserRetrieveDestroyViewSet)
# router.register(r'api/v1/grades', )
# router.register(r'api/v1/grades', GradeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/shikirating/', ShikimoriCreateUpdateApiView.as_view()),
    path('api/v1/users/create/', UserCreateView.as_view()),
    path('api/v1/users/', UserListView.as_view({'get': 'list'})),
    path('api/v1/grade/create/', GradeCreateView.as_view()),
    path('api/v1/grade/create/', GradeUpdateRetrieve.as_view())
]

urlpatterns += router.urls
