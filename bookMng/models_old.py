from django.contrib.auth.models import User
from django.db import models


class MainMenu(models.Model):
    item = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=300, blank=True)  # allow empty if you want
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)

    # IMPORTANT: save uploads under MEDIA_ROOT / 'books'
    # Use ImageField (requires Pillow) so templates can use b.picture.url
    picture = models.ImageField(upload_to='books/', blank=True, null=True)

    # If you don't need this, you can remove it. Kept but optional.
    pic_path = models.CharField(max_length=300, editable=False, blank=True)

    # owner (nullable)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
