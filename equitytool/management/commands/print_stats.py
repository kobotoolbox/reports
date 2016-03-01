import requests
import datetime

from collections import OrderedDict
from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from reporter.models import Rendering

DATE_FORMAT = '%m/%d/%Y'

###############################################################################
########################## User Report Configuration ##########################
###############################################################################
# Fields from `django.contrib.auth.User` to include in the report. Methods that
# don't require arguments can be called by suffixing the method name with `()`,
# e.g. `method_name()`. Django-style, double-underscore-separated relational
# paths, e.g. `related_obj__attribute`, can be traversed.
LOCAL_USER_FIELDS = (
    'first_name',
    'last_name',
    'username',
    'date_joined',
    'last_login',
    'email',
)
# Fields to retrieve from the KoBoCAT profile API and include in the report
KC_PROFILE_FIELDS = ('organization',)

###############################################################################
######################### Project Report Configuration ########################
###############################################################################
RENDERING_FIELDS = (
    'form_name',
    'created',
    'submission_count()',
    'template__name',
)

# Configuration ends here

KC_PROFILE_ENDPOINT = '{}/api/v1/profiles'.format(settings.KC_URL)

def print_tabular(list_of_dicts, stdout):
    # TODO: Handle data that includes tab characters
    if not len(list_of_dicts):
        return
    stdout.write('\t'.join(list_of_dicts[0].keys()))
    for r in list_of_dicts:
        stdout.write('\t'.join(r.values()))

def render_field(obj, field_name):
    if field_name.endswith('()'):
        is_method = True
        field_name = field_name[:-2]
    else:
        is_method = False
    field = get_related_field(obj, field_name)
    if is_method:
        field = field()
    if type(field) is datetime.datetime:
        # Excel compatibility
        return field.strftime(DATE_FORMAT)
    else:
        return str(field)

def get_related_field(obj, field_name):
    # Is there really not a Django utility function for this?
    path = field_name.split('__')
    field = obj
    for p in path:
       field = getattr(field, p)
    return field

def user_report(stdout, stderr):
    stderr.write('Please wait while profiles load slowly from KC...')
    kc_response = requests.get(KC_PROFILE_ENDPOINT)
    kc_profiles = {p['username']: p for p in kc_response.json()}
    stderr.write(' Loading complete!\n')

    user_report = []
    for user in User.objects.all():
        row = OrderedDict()
        try:
            profile = kc_profiles[user.username]
        except KeyError:
            stderr.write(u'No profile for {}!\n'.format(user.username))
            profile = None
        for f in LOCAL_USER_FIELDS:
            row[f] = render_field(user, f)
        for f in KC_PROFILE_FIELDS:
            if profile is not None:
                row[f] = profile[f]
            else:
                row[f] = str(None)
        user_report.append(row)
    print_tabular(user_report, stdout)

def project_report(stdout, stderr):
    project_report = []
    for rendering in Rendering.objects.all():
        row = OrderedDict()
        for f in RENDERING_FIELDS:
            row[f] = render_field(rendering, f)
        project_report.append(row)
    stderr.write('\n')
    print_tabular(project_report, stdout)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--users',
            action='store_true',
            dest='user_report',
            default=False,
            help='Print user report to stdout'),
        make_option(
            '--projects',
            action='store_true',
            dest='project_report',
            default=False,
            help='Print project (`Rendering`) report to stdout'),
    )
    def handle(self, *args, **options):
        if options.get('user_report'):
            user_report(self.stdout, self.stderr) 
        if options.get('project_report'):
            project_report(self.stdout, self.stderr)
