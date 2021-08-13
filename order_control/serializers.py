from rest_framework import serializers

from order_control.models import Purchase, PurchasedItems


class PurchasedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItems
        fields = ('name', 'amount', 'quantity')


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchasedItemsSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['createAt', 'amount', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)
        for item_data in items_data:
            PurchasedItems.objects.create(purchase=purchase, **item_data)
        return purchase


