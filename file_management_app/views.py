from .serializers import ItemSerializer
from .models import Item
from rest_framework import generics


class DeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ImportsView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class NodesView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


