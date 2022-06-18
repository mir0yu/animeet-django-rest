from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView, \
    get_object_or_404

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import User, MatchRequest, MatchedUser
from users.permissions import IsAdminOrIsSelf, IsOwnerOrReadOnly
from users.serializers import UserDetailSerializer, UserCreateSerializer, MatchRequestSerializer, MatchedUsersSerializer


class UserRetrieveUpdateViewSet(RetrieveUpdateAPIView,
                                viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = []


class SelfUserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminOrIsSelf]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(User, pk=request.user.pk)
        serializer = self.get_serializer(instance, many=False)
        return Response(serializer.data)


class UserListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        current_user = self.request.user
        queryset = User.objects.exclude(id=current_user.id, is_admin=True, gender=current_user.gender)
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
        serializer = MatchRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user_id = str(self.request.query_params.get('user_id', None))

        queryset = MatchRequest.objects.all()

        if user_id is not None:
            queryset = queryset.raw(
                'SELECT request.id, request.sender_id AS user1_id, request.receiver_id AS user2_id, match.first_name, '
                'match.last_name, match.email, match.gender, match.bio FROM users_matchrequest request LEFT JOIN '
                'users_matchrequest request2 ON request.receiver_id = request2.sender_id JOIN users_user match ON '
                'request.receiver_id = match.id WHERE request.sender_id = request2.receiver_id AND request.sender_id '
                '= {}'.format(user_id))
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
