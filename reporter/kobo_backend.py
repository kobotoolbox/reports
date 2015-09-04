from social.backends.oauth import BaseOAuth2


KC_URL = 'http://192.168.59.104:8000'


class KoboOAuth2(BaseOAuth2):
    name = 'kobo-oauth2'
    AUTHORIZATION_URL = KC_URL + '/o/authorize/'
    ACCESS_TOKEN_URL = KC_URL + '/o/token/'
    ACCESS_TOKEN_METHOD = 'POST'

    def user_data(self, access_token, *args, **kwargs):
        '''
        Loads user data from API.
        '''
        url = KC_URL + '/api/v1/user'
        return self.get_json(
            url,
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )

    def get_user_details(self, response):
        '''
        Return user details from API.
        '''
        fullname, first_name, last_name = self.get_user_names(
            response.get('name')
        )
        return {
            'username': str(response.get('username')),
            'email': response.get('email'),
            'fullname': fullname,
            'first_name': first_name,
            'last_name': last_name
        }
