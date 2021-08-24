from rest_framework import serializers, pagination

from order_control.models import Purchase, PurchasedItems, BoxTop, Order, Client


class PurchasedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItems
        fields = ('id', 'name', 'amount', 'quantity')


class PurchaseSerializer(serializers.ModelSerializer):

    items = PurchasedItemsSerializer(many=True, read_only=False)

    class Meta:
        model = Purchase
        fields = ('id', 'createAt', 'amount', 'items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)
        for item_data in items_data:
            PurchasedItems.objects.create(purchase=purchase, **item_data)
        return purchase


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model: Client
        fields = "__all__"


class BoxTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxTop
        fields = ('id', 'gift', 'type', 'theme', 'birthdayName', 'amount', 'storedIn')


class OrderSerializer(serializers.ModelSerializer):

    items = BoxTopSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ('id', 'deliveryAt', 'delivered', 'description',
                  'downPayment', 'totalOrder', 'totalPayment', 'client', 'items')

    def create(self, validated_data):
        boxtop_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for boxtop in boxtop_data:
            BoxTop.objects.create(order=order, **boxtop)
        return order


class ClientSerializer(serializers.ModelSerializer):
    client = serializers.RelatedField(many=False, read_only=True)

    class Meta:
        model = Client
        fields = "__all__"