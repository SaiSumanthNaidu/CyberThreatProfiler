from django.db import models

class Threat(models.Model):

    threat_name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100
    )

    risk_score = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.threat_name