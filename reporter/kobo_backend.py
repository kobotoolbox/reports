from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db import transaction
import requests

from reporter.models import UserExternalApiToken

class KoboApiAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        url = '{}authorized_application/authenticate_user/'.format(
            settings.KPI_URL)
        data = {'username': username, 'password': password}
        headers = {'Authorization': 'Token {}'.format(settings.KPI_API_KEY)}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            return
        response_data = response.json()
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
