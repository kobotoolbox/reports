from social.backends.oauth import BaseOAuth2
from django.conf import settings


KC_URL = settings.KC_URL


class KoboOAuth2(BaseOAuth2):
    name = 'kobo-oauth2'
    AUTHORIZATION_URL = KC_URL + '/o/authorize/'
    ACCESS_TOKEN_URL = KC_URL + '/o/token/'
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
