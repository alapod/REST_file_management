from .serializers import ItemSerializer, ItemBatchSerializer, NodeSerializer
from .models import Item
from rest_framework.generics import (
    DestroyAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


class DeleteView(DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class ImportsView(CreateAPIView):
    serializer_class = ItemBatchSerializer

    def update_ancestors(self, parentId, size, update_date):
        parent = Item.objects.get(id=parentId)
        ancestors = parent.get_ancestors(include_self=True)
        for ancestor in ancestors:
            ancestor.size += size
            ancestor.update_date = update_date
            ancestor.save()

    def skip_existing_nodes(self, data):
        ids = [x['id'] for x in data["items"]]
        repeating = []
        for item in ids:
            if Item.objects.filter(id=item).exists():
                repeating.append(item)
        new_data = [x for x in data['items'] if x['id'] not in repeating]
        return {'items': new_data}

    def create(self, request, *args, **kwargs):
        update_date = request.data["updateDate"]
        for i in range(len(request.data["items"])):
            new_data = {"items": [request.data["items"][i]]}
            new_data["items"][-1]["update_date"] = update_date
            new_data = self.skip_existing_nodes(new_data)
            serializer = self.get_serializer(data=new_data)
            try:
                serializer.is_valid(raise_exception=True)
            except ValidationError:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            self.perform_create(serializer)
            if request.data["items"][i]['type'] == 'FILE':
                self.update_ancestors(request.data["items"][i]['parentId'], request.data["items"][i]['size'], update_date)
            headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class NodesView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = NodeSerializer
    throttle_scope = "info"
    a = sorted([1, 2, 6, 3])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatesView(RetrieveAPIView):
    throttle_scope = "info"
    queryset = Item.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NodeHistoryView(ListAPIView):
    throttle_scope = "info"
