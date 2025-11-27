from rest_framework import serializers
from .models import Fridge, Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class FridgeSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Fridge
        fields = ["id", "name", "description", "items"]
        read_only_fields = ['created_at', 'updated_at']
