from django.db import models


class Post(models.Model):

    source = models.CharField(
        max_length=100
    )

    author = models.CharField(
        max_length=100
    )

    content = models.TextField()

    threat_score = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.author