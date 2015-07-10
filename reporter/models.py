from django.db import models
from django.contrib.auth.models import User


class Template(models.Model):
    rmd = models.TextField()


class Rendering(models.Model):
    # I'm putting a user here because each rendering may access
    # private data that relies on the user for authentication.
    user = models.ForeignKey(User)
    template = models.ForeignKey(Template)
    data = models.URLField()
    md = models.TextField()
    html = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def render(self):
        pass
