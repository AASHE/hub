from django.db import models
from django.template.defaultfilters import linebreaks


class Text(models.Model):
    text = models.TextField()

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return linebreaks(self.text)
