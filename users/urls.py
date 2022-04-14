from django.urls import path, include
from users import views
from rest_framework.routers import SimpleRouter, DefaultRouter


router = DefaultRouter()
router.register(r'requests', views.MatchRequestViewSet)
router.register(r'users', views.UserRetrieveDestroyViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('new/', views.UserCreateView.as_view()),
    path('users/', views.UserListView.as_view({'get': 'list'})),
    path('matches/', views.MatchedUsersView.as_view())
]
