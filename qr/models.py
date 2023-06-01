from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.user.email}'
