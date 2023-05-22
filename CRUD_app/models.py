from django.db import models
from django.contrib.auth.models import User

class Box(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boxes', default=None)
    length = models.FloatField(null=False, blank=False)
    breadth = models.FloatField(null=False, blank=False)
    height = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def area(self):
        return self.length * self.breadth

    @property
    def volume(self):
        return self.length * self.breadth * self.height

    def __str__(self):
        return f"Box {self.pk}"

    
