from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemBatchSerializer(serializers.Serializer):
    items = ItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        items = []
        for item in items_data:
            items.append(Item.objects.create(**item))
        return {"items": items}


class NodeSerializer(serializers.Serializer):
    def to_representation(self, instance):
        children_inst = instance.get_children()
        children = []
        if children_inst:
            children = [self.to_representation(child) for child in children_inst]

        result = {
            "children": None,
            "date": instance.update_date,
            "id": instance.id,
            "parentId": None,
            "size": instance.size,
            "type": instance.type,
            "url": instance.url,
        }
        if not instance.parentId:
            result["children"] = children

        elif instance.type == "FILE":
            result["parentId"] = instance.parentId.id

        else:
            result["children"] = children
            result["parentId"] = instance.parentId.id
        return result
