from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"  # email as username field
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = CloudinaryField(
        "image",
        folder="Green_Harvest/users/",
        transformation=[{"width": 800, "height": 800, "crop": "fill", "gravity": "face"}],
        null=True,
        blank=True,
    )
    phone = models.CharField(max_length=20, blank=True)
    street_address = models.TextField()
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
