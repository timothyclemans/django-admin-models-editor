from django.db import models
class Samplemodel(models.Model):
    sample_char_field = models.CharField(max_length=30)

    def __unicode__(self):
        return ''
