from social.backends.oauth import BaseOAuth2


class KoboOAuth2(BaseOAuth2):
    '''
    Backend to connect with Django REST Framework.
    '''
    name = 'kobo'
    AUTHORIZATION_URL = 'https://kc.kobotoolbox.org/o/authorize/confirm/'
    ACCESS_TOKEN_URL = 'https://kc.kobotoolbox.org/o/access_token/'
