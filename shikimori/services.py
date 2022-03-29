from pprint import pprint

from django.forms import model_to_dict
from pyshikiapi import API

from animeet import settings
from shikimori.models import ShikimoriTitleRating, ShikimoriAnimeTitle, ShikimoriID

from shikimori.serializers import ShikimoriIDSerializer, ShikimoriTitleSerializer


def fetchDataFromShikiApi(client_code, ):
    app_name = 'Animeet'
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    client_code = client_code

    api = API(app_name, client_id, client_secret)
    api.fetch_token(client_code)

    access_token = api.token['access_token']
    refresh_token = api.token['refresh_token']

    whoami = api.users.whoami.GET()
    user_rates = api.user_rates().GET(user_id=whoami['id'])

    print(whoami)
    return [user_rates, access_token, refresh_token, whoami['id']]


# def shikiDatatoSerializer(data, request):
#     model = []
#     pprint(data)
#     # print(ShikimoriTitleRating(data[0][0]['target_id'], data[3], data[0][0]['score']))
#     # print(data[0][0][1]['target_id'])
#     for i in range(len(data[0][0])):
#         sat = ShikimoriTitleSerializer(data={'target_id': data[0][i]['target_id']})
#         sid = ShikimoriIDSerializer(data={'shikiID': data[3]})
#         print(sid.data)
#         print(sat.data)
#         if sat.is_valid():
#             sat.save()
#         if sid.is_valid():
#             sid.save()
#         model.append({'title': sat.data.pk, 'owner': sid.data.pk, 'rate': data[0][i]['score']})
#         # sat.save()
#         # sid.save()
#         print(model)
#     return model
