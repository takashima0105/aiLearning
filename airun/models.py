from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TeacherData(models.Model):
    epoch = models.PositiveIntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000)], default=500)
    inputFile = models.FileField(upload_to='inputs/')
    outputFile = models.FileField(upload_to='outputs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AITestData(models.Model):
    test = models.FileField(upload_to='test/')
    json = models.FilePathField(path='json/')
    weight = models.FilePathField(path='weight/')

# Create your models here.
