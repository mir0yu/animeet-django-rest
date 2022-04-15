from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers, fields
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueTogetherValidator

from users.models import User, MatchRequest


class UserDetailSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    # age = serializers.

    # password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'avatar',
                  'age', 'created_at', 'gender']


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    date_of_birth = serializers.DateField()

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'date_of_birth', 'password', 'password2', 'code']
        extra_kwargs = {'password': {'style': {'input_type': 'password'}, 'write_only': True, 'required': True}}

    def create(self, validated_data):
        if self.validated_data['password'] == self.validated_data['password2']:
            validated_data.pop('password2')
            return User.objects.create_user(**validated_data)
        else:
            raise serializers.ValidationError("Password not identical")


class MatchRequestSerializer(serializers.ModelSerializer):
    # sender = serializers.ReadOnlyField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MatchRequest
        fields = ['sender', 'receiver']
        unique_together = (('sender', 'receiver'),)

        validators = [
            UniqueTogetherValidator(queryset=MatchRequest.objects.all(), fields=['sender', 'receiver'])
        ]

    def validate(self, data):
        sender = data.get('sender')
        receiver = data.get('receiver')
        if sender == receiver:
            raise serializers.ValidationError('Fields are the same')
        else:
            return data


class MatchedUsersSerializer(serializers.ModelSerializer):
    user1_id = serializers.IntegerField(required=True)
    user2_id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['user1_id', 'user2_id', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'bio']

# class GradeCreateSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
#     user_id_given = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
#                                                        default=serializers.CurrentUserDefault())
#     user_id_received = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#
#     grade = serializers.ChoiceField(choices=Grade.GRADE_CHOICES)
#
#     class Meta:
#         model = Grade
#         fields = '__all__'
#
#
# class GradeSerializer(serializers.ModelSerializer):
#     user_id_given = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
#                                                        default=serializers.CurrentUserDefault(),
#                                                        validators=[])
#     user_id_received = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), validators=[])
#
#     grade = serializers.ChoiceField(choices=Grade.GRADE_CHOICES)
#
#     class Meta:
#         model = Grade
#         fields = '__all__'
#
#     def update(self, instance, validated_data):
#         user_received = User.objects.get(pk=validated_data['pk'])
#
#         instance.user_id_given = validated_data.pop['user_id_given']
#         instance.grade = validated_data.pop['grade']
#         instance.user_id_received = user_received
#         instance.save()
#
#         return instance
