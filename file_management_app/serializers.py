from rest_framework import serializers
from .models import Item




class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemBatchSerializer(serializers.Serializer):
    items = ItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        items = []
        for item in items_data:
            items.append(Item.objects.create(**item))
        return {'items': items}

class ParentSerializer(serializers.Serializer):
    items = ItemSerializer(many=True)
    def update_or_create(self, parent_id, child_id=0):
        defaults = {'type': 'FOLDER'}
        try:
            obj = Item.objects.get(id=parent_id)
            for key, value in defaults.items():
                setattr(obj, key, value)
                #add child
            obj.save()
        except Item.DoesNotExist:
            new_values = {'parentId': parent_id}
            #add_child
            new_values.update(defaults)
            obj = Item(**new_values)
            obj.save()
        return obj

    def create_relation(self, parent_id, child_id):
        relation = Relations(parent=parent_id, child=child_id)
        relation.save()

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        items = []
        for item in items_data:
            if item['parentId']:
                parent = self.update_or_create(item['parentId'])
                self.create_relation(parent, item['id'])
            ch = Item.objects.create(**item)
           # if item['parentId']:
            #    add_child(child=ch, parent=parent)
            items.append(ch)

        return {'items': items}

class NodeSerializer(serializers.Serializer):

    def to_representation(self, instance):
        children_inst = instance.get_children()

        children = []
        if children_inst:
            children = [self.to_representation(child) for child in children_inst]
        if not instance.parentId:
            return {"children": children,
                "date": instance.update_date,
                "id": instance.id,
                "parentId": None,
                "size": instance.size,
                "type": instance.type,
                "url": instance.url}
        elif instance.type == 'FILE':
            return {"children": None,
                    "date": instance.update_date,
                    "id": instance.id,
                    "parentId": instance.parentId.id,
                    "size": instance.size,
                    "type": instance.type,
                    "url": instance.url}
        else:
            return {"children": children,
                "date": instance.update_date,
                "id": instance.id,
                "parentId": instance.parentId.id,
                "size": instance.size,
                "type": instance.type,
                "url": instance.url}
