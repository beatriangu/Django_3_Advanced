
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class Article(models.Model):
    title = models.CharField(max_length=64, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(auto_now_add=True)
    synopsis = models.CharField(max_length=312, null=False)
    content = models.TextField(null=False)
    published_date = models.DateTimeField() 
    
    def __str__(self):
        return self.title


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['article']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"



