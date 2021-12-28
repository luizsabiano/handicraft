from time import timezone

from rest_framework import serializers, pagination

from order_control.models import Purchase, PurchasedItems, BoxTop, Order, Client, LoyatyCard


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
            box_top = BoxTop.objects.create(order=order, **boxtop)
            self.add_gift_to_loyaty_card(order.client, box_top)
            box_top.order.client.balance += box_top.amount
            box_top.order.client.save()

            # 25/11
            # Caso o cliente seja uma boleira e a arte seja elegível a ganhar um adesivo
            # Verificar se a cliente possui cartão fidelidade
            # ou caso tenha verificar se este ja não esteja finalizado
            # caso falso, inicia um novo cartão
            client = box_top.order.client
            if client.is_cake_maker() and box_top.is_eligible_gift():
                if not LoyatyCard.objects.filter(client=client).exists() or \
                        LoyatyCard.objects.filter(client=client).last().finishedAt:
                    LoyatyCard(client=client).save()

                # Pega o último cartão e adiciona um adesivo
                loyaty_card = LoyatyCard.objects.filter(client=client).last()
                loyaty_card.add_adhesive(loyaty_card, box_top)
            # 25/11

        return order

    @staticmethod
    def add_gift_to_loyaty_card(client, boxtop):
        # check if top is a gift
        if boxtop.is_gift():
            loyaty = LoyatyCard.objects.filter(
                client=client,
                finishedAt__isnull=False,
                giftTopOfCake__isnull=True).order_by('finishedAt')[0]

            # check if loyaty is null
            if loyaty:
                loyaty.giftSave(boxtop)


class ClientSerializer(serializers.ModelSerializer):
    client = serializers.RelatedField(many=False, read_only=True)

    class Meta:
        model = Client
        fields = "__all__"
