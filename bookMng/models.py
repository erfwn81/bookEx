from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class MainMenu(models.Model):
    item = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=300, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.ImageField(upload_to='books/', blank=True, null=True)
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def average_rating(self):
        """Calculate average rating for this book"""
        ratings = self.rating_set.all()
        if ratings:
            return sum(r.stars for r in ratings) / len(ratings)
        return 0


class Comment(models.Model):
    """Comments on books"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.book.name}"


class Rating(models.Model):
    """Star ratings for books (1-5 stars)"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rated {self.book.name} - {self.stars} stars"


class Favorite(models.Model):
    """User's favorite books"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} favorited {self.book.name}"
