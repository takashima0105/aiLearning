from django.db import models

attach = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        verbose_name='添付ファイル',
    )

# Create your models here.
