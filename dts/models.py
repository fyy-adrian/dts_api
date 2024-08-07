from django.db import models
import uuid

def get_random_filename(path):
    def inner(instance, filename):
        extension = filename.split('.')[-1]
        new_filename = f'{uuid.uuid4()}.{extension}'
        return f'{path}/{new_filename}'
    return inner

class Home(models.Model):
    image = models.ImageField(upload_to=get_random_filename('hero'), max_length=255, default='hero/default.jpg')
    active = models.BooleanField(default=False)
    
class Portofolio(models.Model):
    image = models.ImageField(upload_to=get_random_filename('portfolio'), max_length=255, default="portfolio/default.jpg")

class Price(models.Model):
    level = models.CharField(max_length=255,)
    price = models.BigIntegerField(default=0)
    features = models.JSONField()
    special = models.BooleanField(default=False)

class Service(models.Model):
    title = models.CharField(max_length=255,)
    description = models.TextField()
    image = models.ImageField(upload_to=get_random_filename('service'), max_length=255, default="service/default.jpg")

class Contact(models.Model):
    name = models.CharField(max_length=255,)
    email = models.CharField(max_length=255,)
    message = models.TextField(max_length=255)

class Partnership(models.Model):
    name = models.CharField(max_length=255,)
    image = models.ImageField(upload_to=get_random_filename('partnership'), max_length=255, default="partnership/default.jpg")
