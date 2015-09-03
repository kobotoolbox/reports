from social.backends.oauth import BaseOAuth2


class DropboxOAuth2(BaseOAuth2):
    name = 'dropbox-oauth2'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://www.dropbox.com/1/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.dropbox.com/1/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('uid', 'username'),
    ]

    def get_user_details(self, response):
        """Return user details from Dropbox account"""
        fullname, first_name, last_name = self.get_user_names(
            response.get('display_name')
        )
        return {'username': str(response.get('uid')),
                'email': response.get('email'),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://api.dropbox.com/1/account/info',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )
