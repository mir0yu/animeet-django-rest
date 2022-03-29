from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from users.models import User, Grade

from shikimori.models import ShikimoriTitleRating

from users.permissions import IsOwnerOrReadOnly


class UserDetailSerializer(serializers.ModelSerializer):
    # titles = serializers.PrimaryKeyRelatedField(many=True, queryset=ShikimoriTitleRating.objects.all())
    gender = serializers.CharField(source="get_gender_choices", read_only=True)

    # password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'username', 'bio', 'avatar',
                  'date_of_birth', 'last_time_visit', 'code', 'gender']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password', 'code']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            phone_number=validated_data['phone_number'],
            code=validated_data['code'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# class UserListSerializer(serializers.ListSerializer):


class GradeCreateSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    user_id_given = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                       default=serializers.CurrentUserDefault())
    user_id_received = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    grade = serializers.ChoiceField(choices=Grade.GRADE_CHOICES)

    class Meta:
        model = Grade
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    user_id_given = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                       default=serializers.CurrentUserDefault(),
                                                       validators=[])
    user_id_received = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), validators=[])

    grade = serializers.ChoiceField(choices=Grade.GRADE_CHOICES)

    class Meta:
        model = Grade
        fields = '__all__'



