from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)



class Document(models.Model):
    docfile = models.FileField(upload_to='docs/')
    hash = models.TextField()
    upload_time = models.DateTimeField('date uploaded', auto_now_add=True)