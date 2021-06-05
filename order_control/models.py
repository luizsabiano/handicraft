from django.db import models

PAYMENT_CHOICES = (
    ('PP', 'PicPay'),
    ('PIX', 'PIX'),
    ('CC', 'Cartão de Crédito'),
    ('CD', 'Cartão de Débito'),
    ('CASH', 'Dinheiro'),
)


# classe cliente. Atributo balance: se negativo o cliente é devedor, se positivo ele tem haver

class Client (models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome do Cliente')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Telefone')
    picture = models.ImageField(upload_to='clients/', null=True, blank=True, verbose_name='Foto de Perfil')
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    cakeMaker = models.BooleanField(default=False, verbose_name='Boleira')

    def __str__(self):
        return self.name


# classe pedido. Os atributos totalOrder e totalPayment servem para
# reduzir o processamento com consultas futuras onde deseja saber se
# o pedido já está pago, caso não quanto falta ou se tem sobra.
# downPayment - entrada

class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    deliveryAt = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    downPayment = models.DecimalField(max_digits=8, decimal_places=2)
    totalOrder = models.DecimalField(max_digits=8, decimal_places=2)
    totalPayment = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.createdAt, self.totalOrder, self.totalPayment


# Classe topo de bolo. Amount, Valor do topo.
# esta classe funciona como um ítem de pedido

class TopOfCake(models.Model):
    theme = models.CharField(max_length=255)
    birthdayName = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    storedIn = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)


# classe caixas de aniversários

class BirthdayBox(models.Model):
    type = models.CharField(max_length=255, null=True, blank=True)
    theme = models.CharField(max_length=255)
    birthdayName = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    storedIn = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)


# classe cartão fidelidade
# if giftDate has a date and giftTopOfCake filled
# the gift was delivered

class LoyatyCard(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    finishedAt = models.DateTimeField(null=True, blank=True)
    giftDate = models.DateTimeField(null=True,  blank=True)
    giftTopOfCake = models.ForeignKey(TopOfCake, on_delete=models.PROTECT, null=True, blank=True)


# Esta classe funcionar com um ítem de cartão fidelidade
# Uma boleira pode ter vários cartões durante a parceria

class CakeMakerLoyalty(models.Model):
    loyaltyCard = models.ForeignKey(LoyatyCard, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)


# A cada compra de topo a boleira ganha um adesivo
# a cada 10 adevivos ganha um topo de brinde

class Adhesive (models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    topOfCake = models.ForeignKey(TopOfCake, on_delete=models.PROTECT)


class Payment (models.Model):
    type = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    createAt = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)


# classe compras para contabilizar os gastos com compras de materiais

class Purchase(models.Model):
    createAt = models.DateTimeField()


class PurchasedItems(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
