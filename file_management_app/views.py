from .serializers import ItemSerializer, ItemBatchSerializer, ParentSerializer
from .models import Item
from rest_framework.generics import DestroyAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

class DeleteView(DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class ImportsView(CreateAPIView):
    serializer_class = ParentSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)




class NodesView(ListAPIView):
    queryset = Item.objects.all()
    #print(queryset)
    serializer_class = ItemSerializer
    throttle_scope = 'info'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class updates(ListAPIView):
    throttle_scope = 'info'

class NodeHistoryView(ListAPIView):
    throttle_scope = 'info'



