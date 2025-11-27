from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Fridge, Item
from .serializers import FridgeSerializer, ItemSerializer

class FridgeViewSet(viewsets.ModelViewSet):
    serializer_class = FridgeSerializer
    queryset = Fridge.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return self.queryset.filter(fridge__owner=self.request.user)

    def perform_create(self, serializer):
        fridge = serializer.validated_data['fridge']
        if fridge.owner != self.request.user:
            raise PermissionDenied("You cannot add items to someone else's fridge.")
        serializer.save()