from django.db import models
from django.utils import timezone

PAYMENT_CHOICES = (
    ('PP', 'PicPay'),
    ('PIX', 'PIX'),
    ('CC', 'Cartão de Crédito'),
    ('CD', 'Cartão de Débito'),
    ('CASH', 'Dinheiro'),
    ('DCC', 'Depósito Conta Corrente'),
)

BOX_TOP_CHOICES = (
    ('TOPPER', 'TOPO DE BOLO'),
    ('BOX', 'CAIXA BOX'),
    ('TAG', 'TAG'),
    ('OTHERS', 'OUTROS'),
)

GROUP_CHOICES = (
    ('AD', 'ADMINISTRADOR'),
    ('HC', 'ARTESÃ'),
    ('CM', 'BOLEIRA'),
    ('CL', 'CLIENTE')
)

# classe cliente. Atributo balance: se negativo o cliente é devedor, se positivo ele tem haver


class Client (models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, verbose_name='Nome do Cliente')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Telefone')
    picture = models.FileField(upload_to='clients/', null=True, blank=True, verbose_name='Foto de Perfil')
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name='Balanço')
    active = models.BooleanField(default=True, verbose_name="Ativo")
    cakeMaker = models.BooleanField(default=False, verbose_name='Boleira')
    password = models.CharField(max_length=50, verbose_name="Senha")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def is_cake_maker(self):
        if self.cakeMaker: return True
        return False


# classe pedido. Os atributos totalOrder e totalPayment servem para
# reduzir o processamento com consultas futuras onde deseja saber se
# o pedido já está pago, caso não quanto falta ou se tem sobra.
# downPayment - entrada

class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    deliveryAt = models.DateTimeField(null=True, blank=True, verbose_name="Entregar em")
    delivered = models.BooleanField(default=False, verbose_name="Entregue")
    description = models.TextField(max_length=255, null=True, blank=True)
    downPayment = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Entrada R$', null=True, blank=True, default=0.00)
    totalOrder = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Total Pedido R$', null=True, blank=True, default=0.00)
    totalPayment = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Total Pago R$', null=True, blank=True, default=0.00)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="client", verbose_name='Cliente')

    class Meta:
        unique_together = ['client', 'id']
        ordering = ['-id']


    def __str__(self):
        return str(self.id) + ' - '   + self.client.name + ' - ' + self.createdAt.strftime('%m/%d/%Y')


# Classe topo de bolo / caixa box. Amount, Valor do topo.
# esta classe funciona como um ítem de pedido

class BoxTop(models.Model):
    gift = models.BooleanField(default=False, verbose_name="Brinde?")
    type = models.CharField(max_length=255, choices=BOX_TOP_CHOICES, verbose_name="Tipo")
    theme = models.CharField(max_length=255)
    birthdayName = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name='Valor total R$')
    description = models.CharField(max_length=255, null=True, blank=True)
    storedIn = models.FileField(upload_to='boxes/', null=True, blank=True, verbose_name='Figura')
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT)

    class Meta:
        unique_together = ['order', 'id']
        ordering = ['id']

    def is_gift(self):
        if self.gift:
            return True
        return False

    def is_eligible_gift(self):
        if self.type == "TOPPER" and not self.is_gift():
            return True
        return False


# classe cartão fidelidade
# if giftDate has a date and giftTopOfCake filled
# the gift was delivered


class LoyatyCard(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    adhesiveCount = models.IntegerField(null=True, blank=True, default=0)
    # Remover adhesiveCount -> Campo computado
    finishedAt = models.DateTimeField(null=True, blank=True, default=None)
    giftDate = models.DateTimeField(null=True,  blank=True)
    # Remover o campo giftDate -> campo computado, a data do brinde é a data da entrega do item.
    giftTopOfCake = models.ForeignKey(BoxTop, on_delete=models.PROTECT, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    isDelivered = models.BooleanField(default=False, verbose_name="Está entregue?")

    def __str__(self):
        return 'Id: %d - Cliente: %s -  Adevivos: %d' % (self.id, self.client, self.adhesiveCount)

    def giftSave(self, boxtop):
        self.giftDate = timezone.now()
        self.giftTopOfCake = boxtop
        self.save()

    def filter_eligible_loyaty_card(self, client):
        loyaty = self.objects.filter(
            client=client,
            finishedAt__isnull=False,
            giftTopOfCake__isnull=True).order_by('finishedAt')[0]
        return loyaty

    def add_adhesive(self, loyatyCard, box_top):
        loyatyCard.adhesiveCount += 1
        loyatyCard.save()
        adhesive = Adhesive(topOfCake=box_top, loyatyCard=loyatyCard)
        adhesive.save()

        # Caso complete 10 adesivos cria um novo cartao fidelidade.
        if loyatyCard.adhesiveCount > 9:
            loyatyCard.finishedAt = timezone.now()
            loyatyCard.save()

        # Fechar cartao fidelidade com 10 adesivos


# A cada compra de topo a boleira ganha um adesivo
# a cada 10 adevivos ganha um topo de brinde

class Adhesive (models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    topOfCake = models.ForeignKey(BoxTop, on_delete=models.PROTECT)
    loyatyCard = models.ForeignKey(LoyatyCard, on_delete=models.PROTECT)

    def __str__(self):
        return 'Criado em: %s - Cartao nº: %s' % (str(self.createdAt)[0:10], self.loyatyCard)


class Payment (models.Model):
    type = models.CharField(max_length=255, choices=PAYMENT_CHOICES, verbose_name="Tipo")
    createAt = models.DateField(auto_now_add=False, verbose_name="Pago em")
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor")
    downPayment = models.BooleanField(default=False, verbose_name='Entrada')
    order = models.ForeignKey(Order, on_delete=models.PROTECT)


# classe compras para contabilizar os gastos com compras de materiais

class Purchase(models.Model):
    createAt = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ['-id']


class PurchasedItems(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.PROTECT)

    class Meta:
        unique_together = ['purchase', 'id']
        ordering = ['id']

    def __str__(self):
        return '%d: %s: %d:  %d' % (self.id, self.name, self.quantity, self.amount)

