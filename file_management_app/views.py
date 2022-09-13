from .serializers import ItemSerializer, ImportSerializer
from .models import Item, Import
from rest_framework import generics


class DeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ImportsView(generics.CreateAPIView):
    queryset = Import.objects.all()
    serializer_class = ImportSerializer


class NodesView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


