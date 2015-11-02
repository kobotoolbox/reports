from social.backends.oauth import BaseOAuth2
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db import transaction
import requests
import json

from reporter.models import UserExternalApiToken

KC_URL = settings.KC_URL


class KoboOAuth2(BaseOAuth2):
    name = 'kobo-oauth2'
    AUTHORIZATION_URL = settings.OAUTH2_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.OAUTH2_ACCESS_TOKEN_URL
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    ID_KEY = 'username'

    def user_data(self, access_token, *args, **kwargs):
        '''
        Loads user data from API.
        '''
        url = KC_URL + '/api/v1/user'
        data = self.get_json(
            url,
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )
        return data

    def get_user_details(self, response):
        '''
        Return user details from API.
        '''
        fullname, first_name, last_name = self.get_user_names(
            response.get('name')
        )
        user_details = {
            'username': str(response.get('username')),
            'email': response.get('email'),
            'fullname': fullname,
            'first_name': first_name,
            'last_name': last_name
        }
        return user_details

class KoboApiAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        url = '{}authorized-application/authenticate-user/'.format(
            settings.KPI_URL)
        data = {'username': username, 'password': password}
        headers = {'Authorization': 'Token {}'.format(settings.KPI_API_KEY)}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            return
        response_data = json.loads(response.content)
        assert username == response_data['username']
        user = User.objects.get_or_create(username=username)[0]
        user_attributes_to_set = (
            'first_name',
            'last_name',
            'email',
            'is_active',
            'last_login',
            'date_joined'
            #'is_staff',
            #'is_superuser',
        )
        for attribute in user_attributes_to_set:
            setattr(user, attribute, response_data[attribute])
        user.save()
        # Record the token returned by KPI, which will be used to access the
        # KC API
        with transaction.atomic():
            token_storage = UserExternalApiToken.objects.get_or_create(
                user=user)[0]
            token_storage.key = response_data['token']
            token_storage.save()
        return user
