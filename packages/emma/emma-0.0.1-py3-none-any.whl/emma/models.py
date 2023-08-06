from django.db import models

from .storage import ContentAddressableStorage


class Screenshot(models.Model):
    display = models.IntegerField()
    time = models.DateTimeField()
    image = models.ImageField(
        upload_to='screenshots/%Y/%m/%d/%H/%M/',
        storage=ContentAddressableStorage,
    )
