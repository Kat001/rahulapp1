from django.db import models

# Create your models here.

class News(models.Model):
    first_line = models.TextField(max_length=500,null=True,blank=True)
    second_line = models.TextField(max_length=500,null=True,blank=True)
    third_line = models.TextField(max_length=500,null=True,blank=True)
    fourth_line = models.TextField(max_length=500,null=True,blank=True)
