from django.db import models
from django.conf import settings

Users = settings.AUTH_USER_MODEL

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateField('Created', auto_now_add=True)
    update_at = models.DateField('Updated', auto_now=True)
    isCompleted = models.BooleanField(default=False)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    compdate = models.DateField()
    userId = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField('Created', auto_now_add=True)
    update_at = models.DateField('Updated', auto_now=True)
    userId = models.CharField(max_length=100)   
    def __str__(self):
        return self.title

class MainPermisions(models.Model):
    name = models.CharField(max_length=100)
    content_type_id = models.CharField(max_length=100)
    created_at = models.DateField('Created', auto_now_add=True)
    update_at = models.DateField('Updated', auto_now_add=True)
    def __str__(self):
        return self.name


class Permisions(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    permisions_id = models.ForeignKey(MainPermisions, on_delete=models.CASCADE)
    created_at = models.DateField('Created', auto_now_add=True)
    update_at = models.DateField('Updated', auto_now_add=True)
    # def __str__(self):
    #     return self.title



