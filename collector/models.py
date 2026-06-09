from django.db import models


class Feed(models.Model):

    source = models.CharField(
        max_length=100
    )

    threat_type = models.CharField(
        max_length=100
    )

    severity = models.CharField(
        max_length=50
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.source