from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Fridge(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fridges')
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class Item(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()

    time_stored = models.DateTimeField(default=timezone.now)

    best_before = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} in {self.fridge.name}"
