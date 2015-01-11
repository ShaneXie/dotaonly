from django.db import models

# Create your models here.

class stream_sites(models.Model):
    site_name = models.CharField(max_length=20)
    site_code = models.IntegerField()

class streams(models.Model):
    roomid = models.CharField(max_length=20)
    anchorname = models.CharField(max_length=20)
    website = models.ForeignKey(stream_sites)
