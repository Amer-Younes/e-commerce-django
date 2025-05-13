from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save



class User(AbstractUser):
    email = models.EmailField(unique=True )
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Us"


    def __str__(self):
        return self.full_name


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200 , null=True , blank=True)
    bio = models.TextField(null=True , blank=True)
    image = models.ImageField(upload_to="profile_pics/" , null=True , blank=True )
    phone = models.CharField(max_length=30 , null=True , blank=True)
    address = models.TextField(null=True , blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.full_name


def create_profile(sender , instance , created , **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_profile(sender , instance , **kwargs):
    instance.profile.save()

post_save.connect(create_profile , sender=User)
post_save.connect(save_profile , sender=User)