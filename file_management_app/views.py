from .serializers import ItemSerializer, ItemBatchSerializer, NodeSerializer
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
    serializer_class = ItemBatchSerializer

    def create(self, request, *args, **kwargs):
        update_date = request.data['updateDate']
        for i in range(len(request.data["items"])):
            new_data = {'updateDate': update_date, 'items': [request.data["items"][i]]}
            serializer = self.get_serializer(data=new_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class NodesView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = NodeSerializer
    throttle_scope = 'info'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdatesView(ListAPIView):
    throttle_scope = 'info'

class NodeHistoryView(ListAPIView):
    throttle_scope = 'info'

# 1) Find the bad case
# 2) Recursive CTE Postgresql (Trees)
#    django execute raw query
# 3)

# result = {'children': []}
# def rec_descendants(target_id, result: Dict)
#     item = Item.objects.get(pk=target_id)
#     result['parent_id'] = item.pk
#     # ... todo add other fields
#     relations_qs = Relations.objects.filter(parent=target_id)
#     for it in relations_qs:
#         child_result = {'children': []}
#         rec_descendants(it.child_id, child_result)
#         result['children'].append(child_result)
#     return result
#
# return Response(self.form_output(instance), status=status.HTTP_200_OK)