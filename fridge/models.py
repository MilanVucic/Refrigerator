from django.db import models
from django.contrib.auth.models import User

class Fridge(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Item(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    stored_at = models.DateTimeField(auto_now_add=True)
    best_before = models.DateField()
