import decimal
from datetime import date, timedelta

from decimal import Decimal
from rest_framework import viewsets, status, pagination
from rest_framework.response import Response

from order_control.models import Purchase, PurchasedItems, Order, BoxTop, Client
from order_control.serializers import PurchaseSerializer, PurchasedItemsSerializer, OrderSerializer, BoxTopSerializer, \
    ClientSerializer

import json


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def create(self, request, *args, **kwargs):
        purchaseSerializer = PurchaseSerializer(data=request.data)
        if purchaseSerializer.is_valid():
            purchaseSerializer.save()
            data = purchaseSerializer.data
            headers = self.get_success_headers(purchaseSerializer.data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(purchaseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def destroy(self, request, *args, **kwargs):

            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)


class PurchasedItemsViewSet(viewsets.ModelViewSet):
    serializer_class = PurchasedItemsSerializer
    queryset = PurchasedItems.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # subtrai o item do total em purchases
        item = PurchasedItems.objects.get(id=serializer.data['id'])
        item.purchase.amount -= decimal.Decimal(serializer.data['amount'])
        item.purchase.save()
        # -------------------------------------
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrdersViewSet(viewsets.ModelViewSet):
    # Classe a ser serializada
    serializer_class = OrderSerializer
    #queryset = Order.objects.all()

    today = date.today()
    td = timedelta(15)
    initial_date = today - td
    final_date = today + td
    queryset = Order.objects.filter(deliveryAt__range=(initial_date, final_date)).order_by('client')

    def create(self, request, *args, **kwargs):
        dataDict = {}
        dataDict['deliveryAt'] = request.data['deliveryAt']
        #print("DeliveryAt", dataDict['deliveryAt'])
        dataDict['delivered'] = json.loads(request.data['delivered'].lower())

        if request.data['description'] == 'null':
            dataDict['description'] = json.loads(request.data['description'])
        else:
            dataDict['description'] = request.data['description']

        dataDict['totalOrder'] = Decimal(json.loads(request.data['totalOrder']))
        dataDict['client'] = json.loads(request.data['client'])
        dataDict['items'] = json.loads(request.data['items'])

        print("dataDict", dataDict)
        print('request.data', request.data)


        if request.FILES:
            file = request.FILES
            print("files: ", file)
            for key in range(len(dataDict['items'])):
                if dataDict['items'][key]['storedIn']:
                    dataDict['items'][key]['storedIn'] = file[dataDict['items'][key]['storedIn']]

        orderSerializer = OrderSerializer(data=dataDict)

        if orderSerializer.is_valid():
            orderSerializer.save()
            data = orderSerializer.data
            headers = self.get_success_headers(orderSerializer.data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(orderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemsViewSet(viewsets.ModelViewSet):
    serializer_class = BoxTopSerializer
    queryset = BoxTop.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # subtrai o item do total em orders
        item = BoxTop.objects.get(id=serializer.data['id'])
        item.order.totalOrder -= decimal.Decimal(serializer.data['amount'])
        item.order.save()
        # -------------------------------------
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def to_representation(self, instance):
        self.fields['client'] = ClientSerializer(read_only=True)
        return super(OrderSerializer, self).to_representation(instance)


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
