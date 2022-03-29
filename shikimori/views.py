from pprint import pprint

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shikimori.serializers import ShikimoriRatingSimpleSerializer

from shikimori.services import fetchDataFromShikiApi


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
            # print(serializer_data)
            # print(i, "\n")
        serializer = ShikimoriRatingSimpleSerializer(data=serializer_data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
