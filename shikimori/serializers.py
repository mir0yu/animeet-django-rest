from rest_framework import serializers

from shikimori.models import ShikimoriTitleRating

from shikimori.models import ShikimoriID, ShikimoriAnimeTitle

from users.models import User


class ShikimoriIDSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    # print(owner)

    class Meta:
        model = ShikimoriID
        fields = ['shikiID', 'owner']
        extra_kwargs = {
            'shikiID': {'validators': []},
        }


class ShikimoriTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShikimoriAnimeTitle
        fields = ['target_id', ]
        extra_kwargs = {
            'target_id': {'validators': []},
        }


class ShikimoriRatingSimpleSerializer(serializers.ModelSerializer):
    title = ShikimoriTitleSerializer()
    owner = ShikimoriIDSerializer()

    class Meta:
        model = ShikimoriTitleRating
        fields = ['title', 'owner', 'rate']

    def create(self, validated_data):
        anime_title_data = validated_data.pop('title')
        shiki_id_data = validated_data.pop('owner')
        title, _title = ShikimoriAnimeTitle.objects.update_or_create(**anime_title_data)
        owner, _owner = ShikimoriID.objects.update_or_create(**shiki_id_data)
        instance = ShikimoriTitleRating.objects.create(title=title, owner=owner, **validated_data)
        return instance

# class ShikimoriCreateUpdateSerializer(serializers.Serializer):
#
#     def create(self, validated_data):


# class ShikimoriTitleApiSerializer(serializers.Serializer):
