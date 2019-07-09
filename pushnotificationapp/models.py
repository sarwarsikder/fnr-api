from django.db import models


class Subscribers(models.Model):
    endpoint = models.TextField(max_length=2000)
    expirationTime = models.DateTimeField(null=True)
    keys = models.TextField(max_length=2000)
    user_id = models.IntegerField(null=False)
    device = models.CharField(max_length=512)

