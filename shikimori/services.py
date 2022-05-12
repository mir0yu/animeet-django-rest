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


