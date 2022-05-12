from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import User, MatchRequest, MatchedUser
from users.permissions import IsAdminOrIsSelf, IsOwnerOrReadOnly
from users.serializers import UserDetailSerializer, UserCreateSerializer, MatchRequestSerializer, MatchedUsersSerializer


class UserRetrieveUpdateViewSet(RetrieveUpdateAPIView,
                                viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminOrIsSelf, ]


class UserListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        current_user = self.request.user
        # genre = self.request.query_params.get('genre', None)
        # radius = self.request.query_params.get('radius', 5)
        queryset = User.objects.exclude(id=current_user.id, is_admin=True, gender=current_user.gender)

        # if genre is not None:
        #   queryset = queryset.filter(genre=genre)

        return queryset


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny, ]


class MatchRequestViewSet(viewsets.ModelViewSet):
    queryset = MatchRequest.objects.all()
    serializer_class = MatchRequestSerializer


class MatchedUsersView(generics.ListAPIView):
    queryset = MatchedUser.objects.all()
    serializer_class = MatchedUsersSerializer

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = MatchRequestSerializer(list(queryset), many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)

        queryset = MatchRequest.objects.all()

        if user_id is not None:
            # queryset.filter(sender_id=user_id)
            queryset = queryset.raw(
                'SELECT request.id, request.sender_id AS user1_id, request.receiver_id AS user2_id, match.first_name, '
                'match.last_name, match.email, match.gender, match.bio FROM users_matchrequest request LEFT JOIN '
                'users_matchrequest request2 ON request.receiver_id = request2.sender_id JOIN users_user match ON '
                'request.receiver_id = match.id WHERE request.sender_id = request2.receiver_id AND request.sender_id = %s',
                user_id)
        else:
            queryset = queryset.raw(
                'SELECT request.id, request.sender_id AS user1_id, request.receiver_id AS user2_id, match.first_name, '
                'match.last_name, match.email, match.gender, match.bio FROM users_matchrequest request LEFT JOIN '
                'users_matchrequest request2 ON request.receiver_id = request2.sender_id JOIN users_user match ON '
                'request.receiver_id = match.id WHERE request.sender_id = request2.receiver_id AND request.sender_id '
                '< request.receiver_id')

        return queryset

# class GradeCreateView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = GradeCreateSerializer
#     permissions = [IsOwnerOrReadOnly, IsAuthenticated, ]
#
#
# class GradeUpdateRetrieve(RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = GradeSerializer
#     permissions = [IsOwnerOrReadOnly, IsAuthenticated, ]
