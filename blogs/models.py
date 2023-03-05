from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=20)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Blog(models.Model):
    tittle = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.tittle


class Images(models.Model):
    image = models.ImageField(upload_to='blogpost/')
    blog= models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog')

class Likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bloglike')
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='bloglike')
    created_at = models.DateTimeField(auto_now_add=True)

class Dislikes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogdislike')
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blogdislike')
    created_at = models.DateTimeField(auto_now_add=True)
