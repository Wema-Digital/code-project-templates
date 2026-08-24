from django.db import models


class Ping(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ping #{self.pk} at {self.created_at:%Y-%m-%d %H:%M:%S}"
