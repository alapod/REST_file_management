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
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class ImportsView(CreateAPIView):
    serializer_class = ItemBatchSerializer

    def update_ancestors(self, parentId, size, update_date):
        parent = Item.objects.get(id=parentId)
        ancestors = parent.get_ancestors(include_self=True)
        for ancestor in ancestors:
            try:
                ancestor.size += size
                ancestor.update_date = update_date
                ancestor.save()
            except:
                continue        #add logging

    def skip_existing_nodes(self, data):
        ids = [x["id"] for x in data["items"]]
        repeating = []
        for item in ids:
            if Item.objects.filter(id=item).exists():
                repeating.append(item)
        new_data = [x for x in data["items"] if x["id"] not in repeating]
        return {"items": new_data}

    def create(self, request, *args, **kwargs):
        update_date = request.data["updateDate"]
        for i, item in enumerate(request.data["items"]):
            new_data = {"items": [item]}
            new_data["items"][-1]["update_date"] = update_date
            new_data = self.skip_existing_nodes(new_data)
            serializer = self.get_serializer(data=new_data)
            try:
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            except ValidationError:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            if item["type"] == "FILE":
                self.update_ancestors(
                    item["parentId"],
                    item["size"],
                    update_date,
                )
            headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class NodesView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = NodeSerializer
    throttle_scope = "info"
    a = sorted([1, 2, 6, 3])

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)



class UpdatesView(RetrieveAPIView):
    throttle_scope = "info"
    queryset = Item.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)



class NodeHistoryView(ListAPIView):
    throttle_scope = "info"
