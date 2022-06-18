from pprint import pprint
import pandas as pd
import turicreate as tc

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shikimori.models import ShikimoriTitleRating, ShikimoriID
from shikimori.serializers import ShikimoriRatingSimpleSerializer

from shikimori.services import fetchDataFromShikiApi
from users.models import User
from users.serializers import UserDetailSerializer


class ShikimoriCreateUpdateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        shikidata = fetchDataFromShikiApi(request.user.code)
        pprint(shikidata)
        serializer_data = []
        for i in range(len(shikidata[0])):
            serializer_data.append({'title': {'target_id': shikidata[0][i]['target_id']},
                                    'owner': {'shikiID': shikidata[3], 'owner': request.user.id},
                                    'rate': shikidata[0][i]['score']})
        serializer = ShikimoriRatingSimpleSerializer(data=serializer_data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        shikidata = fetchDataFromShikiApi(request.user.code)
        pprint(shikidata)
        serializer_data = []
        for i in range(len(shikidata[0])):
            serializer_data.append({'title': {'target_id': shikidata[0][i]['target_id']},
                                    'owner': {'shikiID': shikidata[3], 'owner': request.user.id},
                                    'rate': shikidata[0][i]['score']})
        serializer = ShikimoriRatingSimpleSerializer(data=serializer_data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ShikimoriListUsersRating(ListAPIView):
    queryset = ShikimoriTitleRating.objects.all().values('title_id', 'owner_id', 'rate')

    serializer_class = UserDetailSerializer

    def get_queryset(self):
        queryset = ShikimoriTitleRating.objects.all().values('title_id', 'owner_id', 'rate')
        queryset2 = ShikimoriID.objects.all().values('id', 'owner')
        data = pd.DataFrame(list(queryset))
        data2 = pd.DataFrame(list(queryset2))
        actions2 = tc.SFrame(data2)
        actions = tc.SFrame(data)
        training_data, validation_data = tc.recommender.util.random_split_by_user(
            actions.join(actions2, on={'owner_id': 'id'}, how='right'), 'owner', 'title_id')
        model = tc.factorization_recommender.create(training_data, 'owner', 'title_id', target='rate')
        similar = model.get_similar_users(users=[self.request.user.pk])['similar']
        return User.objects.all().filter(pk__in=similar)
