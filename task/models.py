from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description= models.TextField(blank=True)
    created= models.DateTimeField(auto_now_add=True)
    datecomplete= models.DateTimeField(null=True, blank=True) #dato opcional para vista de admin no para la base de datos
    important= models.BooleanField(default=False)   #por defecto las tareas no son importantes
    user= models.ForeignKey(User, on_delete=models.CASCADE) #borrado de tablas cuando se borra el user

    def __str__(self):
        return self.title + '- de ' + self.user.username
    