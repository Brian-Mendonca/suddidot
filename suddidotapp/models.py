from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from unidecode import unidecode
from tinymce.models import HTMLField
from django.utils import timezone
from django.utils.timezone import now

# Category Model 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# News Article Model
class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    categories = models.ManyToManyField(Category, related_name="articles")  
    content = HTMLField()
    image = models.ImageField(upload_to='news_images/',)
    is_trending = models.BooleanField(default=False)  
    views = models.IntegerField(default=1)
    published_at = models.DateTimeField(default=now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
# Comment model
class Comment(models.Model):
    news_article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}: {self.message[:200]}"