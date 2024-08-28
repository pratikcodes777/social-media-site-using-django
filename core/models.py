from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.CharField(max_length=100 , blank=True)
    profile_img = models.ImageField(upload_to='profile' , default='default.jpeg')
    location = models.CharField(max_length=50 , blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

