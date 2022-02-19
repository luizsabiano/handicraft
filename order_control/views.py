import json

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView, DetailView
from rest_framework import pagination
from rest_framework.response import Response
from handicraft import settings
from order_control.form import ClientForm, OrderForm, BoxTopForm, PaymentForm
from order_control.models import Client, Order, BoxTop, LoyatyCard, Adhesive, Payment, Purchase
from datetime import datetime, date, timedelta
import calendar


def client_eligible_gift(request):

    eligible = "False"
    adhesives_quantity = "0"
    client_id = int(json.loads(request.body))
    client = Client.objects.get(id=client_id)

    loyaty = LoyatyCard.objects.filter(
        client=client,
        finishedAt__isnull=False,
        giftTopOfCake__isnull=True).order_by('finishedAt')

    if loyaty:
        eligible = "True"
    else:
        loyaty = LoyatyCard.objects.filter(
            client=client,
            finishedAt__isnull=True,
            giftTopOfCake__isnull=True).order_by('finishedAt')
        if loyaty:
            adhesives_quantity = loyaty[0].adhesiveCount

    return HttpResponse(
        json.dumps({'eligible': eligible, 'adhesives_quantity': adhesives_quantity}),
        content_type="application/json"
    )


class LoginView(TemplateView):
    template_name = 'order_control/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            django_login(request, user)
            return redirect('/')  # redirect é um atalho para HttpResponseRedirect
        message = 'Credenciais Inválidas'
        return self.render_to_response({'message': message})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'order_control/index.html'

    def post(self, request, *args, **kwargs):
        dataConsulta = request.POST.get('message')
        baseDate = datetime.strptime(dataConsulta + '-01', '%Y-%m-%d').date()
        initialDate = baseDate.strftime("%Y-%m-%d")
        monthRange = calendar.monthrange(baseDate.year, baseDate.month)

        finalDate = datetime.strptime(dataConsulta + '-' + str(monthRange[1]), '%Y-%m-%d').date().strftime("%Y-%m-%d")
        payments = Payment.objects.filter(createAt__range=(initialDate, finalDate)).order_by('createAt')

        purchases = Purchase.objects.all().order_by('createAt').filter(createAt__range=(initialDate, finalDate))
        totalPayments = payments.aggregate(Sum('amount'))

        # loyatyCard = LoyatyCard.objects.filter(finishedAt__isnull=False,
        #                     giftTopOfCake__isnull=True).order_by('client')
        loyatyCard = LoyatyCard.objects.filter(finishedAt__isnull=False,
                            giftTopOfCake__isnull=True).values('client', 'client__name' ).annotate(total=Count('client')).order_by('total')

        print("loyatCard --> ", list(loyatyCard))

        return JsonResponse({'payments': list(payments.values('id', 'type', 'createAt', 'amount',
                                                              'order__client__id',
                                                              'order__client__name',
                                                              'order__client__cakeMaker',
                                                              'order__client__balance')),
                             'totalPayments': totalPayments,
                             'purchases': list(purchases.values()),
                             'loyatyCardsToGift': list(loyatyCard.values('client', 'client__name', 'total'))
                             })


class FormSubmittedIncontextMixin:
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, form_submitted=True))


class ClientCreateView(LoginRequiredMixin, FormSubmittedIncontextMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'order_control/client/create.html'

    # para não entrar na página de detalhes e usar a list.
    success_url = reverse_lazy('order_control:order_create')

    def form_valid(self, form):
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, FormSubmittedIncontextMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'order_control/client/update.html'
    success_url = reverse_lazy('order_control:client_list', )


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'order_control/client/list.html'


@login_required(login_url=reverse_lazy('order_control:login'))
def client_destroy(request, id):
    client = Client.objects.get(id=id)
    if request.method == 'GET':
        form = ClientForm(instance=client)
    else:
        client.delete()
        return redirect(reverse('order_control:client_list'))
    return render(request, 'order_control/client/destroy.html', {'client': client, 'form': form})


@login_required(login_url=reverse_lazy('order_control:login'))
def client_details(request, id):
    client = Client.objects.get(id=id)
    order = Order.objects.filter(client=client).order_by('delivered', 'deliveryAt')
    loyatyCard = LoyatyCard.objects.filter(client=client).order_by('finishedAt', 'giftDate')
    return render(request, 'order_control/client/detail.html', {'client': client, 'orders': order, 'loyatyCards':loyatyCard})


# ---------------------------------------------------------------- -----

@login_required(login_url=reverse_lazy('order_control:login'))
def order_create_vue(request):
    form_submitted = False
    if request.method == 'GET':
        form = OrderForm()
        box_top_form = BoxTopForm()
    else:
        form_submitted = True
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            box_top_form = BoxTopForm()
            box_top = BoxTop.objects.filter(order=order)
            return render(request, 'order_control/order/order_add_items.html',
                {'order': order, 'box_top_form': box_top_form, 'client': order.client, 'box_top': box_top})
    return render(request, 'order_control/order/create_order.html', {'form': form, 'form_submitted': form_submitted, 'box_top_form': box_top_form})


@login_required(login_url=reverse_lazy('order_control:login'))
def order_create(request):
    form_submitted = False
    if request.method == 'GET':
        form = OrderForm()
    else:
        form_submitted = True
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            box_top_form = BoxTopForm()
            box_top = BoxTop.objects.filter(order=order)
            return render(request, 'order_control/order/order_add_items.html',
                {'order': order, 'box_top_form': box_top_form, 'client': order.client, 'box_top': box_top})
    return render(request, 'order_control/order/create.html', {'form': form, 'form_submitted': form_submitted})


def order_add_items(request):

    if request.method == 'POST':
        form = BoxTopForm(request.POST, request.FILES)
        if form.is_valid():
            box_top = form.save(commit=False)
            box_top.order = Order.objects.get(id=request.POST['order'], )
            box_top.save()
            box_top.order.totalOrder += box_top.amount
            box_top.order.save()
            box_top.order.client.balance += box_top.amount
            box_top.order.client.save()

            client = box_top.order.client

            if box_top.gift:

                loyaty = LoyatyCard.objects.filter(
                            client=client,
                            finishedAt__isnull=False,
                            giftTopOfCake__isnull=True).order_by('finishedAt')[0]

                if loyaty:
                    loyaty.giftSave(box_top)

            # 25/11
            # Caso o cliente seja uma boleira e a arte seja elegível a ganhar um adesivo
            # Verificar se a cliente possui cartão fidelidade
            # ou caso tenha verificar se este ja não esteja finalizado
            # caso falso, inicia um novo cartão

            if client.is_cake_maker() and box_top.is_eligible_gift():
                if not LoyatyCard.objects.filter(client=client).exists() or \
                        LoyatyCard.objects.filter(client=client).last().finishedAt:
                    LoyatyCard(client=client).save()

                # Pega o último cartão e adiciona um adesivo
                loyaty_card = LoyatyCard.objects.filter(client=client).last()
                loyaty_card.add_adhesive(loyaty_card, box_top)
            # 25/11

            box_top_json = serializers.serialize("json", BoxTop.objects.filter(order=box_top.order.id))
            message = {"top_box": box_top_json}
            return HttpResponse(
                json.dumps(message),
                content_type="application/json"
            )

# ---------------------------------------------------------------- -----


@login_required(login_url=reverse_lazy('order_control:login'))
def order_update(request, id):
    form_submitted = False
    order = Order.objects.get(id=id)
    items_order = BoxTop.objects.filter(order=order)
    if request.method == 'GET':
        form = OrderForm(instance=order)
    else:
        form_submitted = True
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            box_top_form = BoxTopForm()
            return render(request, 'order_control/order/order_add_items.html',
                          {'order': order, 'box_top_form': box_top_form, 'client': order.client, 'box_top': items_order })
    return render(request, 'order_control/order/update.html',
                  {'order': order, 'form': form, 'items_order': items_order, 'form_submitted': form_submitted})


@login_required(login_url=reverse_lazy('order_control:login'))
def order_details(request, id):
    order = Order.objects.get(id=id)
    order_items = BoxTop.objects.filter(order=order)
    return render(request, 'order_control/order/detail.html',
                  {'order': order, 'order_items': order_items})


@login_required(login_url=reverse_lazy('order_control:login'))
def order_items_details(request, id):
    order_item = BoxTop.objects.get(id=id)
    return render(request, 'order_control/order/item_detail.html', {'order_item': order_item})


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_control/order/list.html'
    ordering = ['client', 'delivered', 'deliveryAt']

    def get_queryset(self):
        today = date.today()
        td = timedelta(45)
        initial_date = today - td
        final_date = today + td
        return Order.objects.filter(deliveryAt__range=(initial_date, final_date))


@login_required(login_url=reverse_lazy('order_control:login'))
def order_destroy(request, id):
    order = Order.objects.get(id=id)
    items_order = BoxTop.objects.filter(order=order)
    if request.method == 'GET':
        form = OrderForm(instance=order)
    else:
        if not items_order:
            order.delete()
        return redirect(reverse('order_control:order_list'))

    return render(request, 'order_control/order/destroy.html',
                      {'order': order, 'form': form, 'items_order': items_order})


@login_required(login_url=reverse_lazy('order_control:login'))
def order_items_update(request, id):
    form_submitted = False
    box_top = BoxTop.objects.get(id=id)
    if request.method == 'GET':
        form = BoxTopForm(instance=box_top)
    else:
        box_top.order.totalOrder -= box_top.amount
        box_top.order.client.balance -= box_top.amount
        form_submitted = True
        form = BoxTopForm(request.POST, request.FILES, instance=box_top)
        if form.is_valid():
            box_top.order.save()
            box_top.order.client.save()
            form.save()
            box_top.order.totalOrder += box_top.amount
            box_top.order.save()
            box_top.order.client.balance += box_top.amount
            box_top.order.client.save()

            return redirect(reverse('order_control:order_update', args=(box_top.order.id,)))

    return render(request, 'order_control/order/update_items.html',
                  {'box_top_form': form, 'box_top': box_top, 'form_submitted': form_submitted})


@login_required(login_url=reverse_lazy('order_control:login'))
def order_items_destroy(request, id):
    box_top = BoxTop.objects.get(id=id)
    if request.method == 'GET':
        form = BoxTopForm(instance=box_top)
        return render(request, 'order_control/order/destroy_items.html', {'box_top': box_top, 'box_top_form': form})
    else:
        if box_top.gift:
            loyaties = LoyatyCard.objects.filter(giftTopOfCake=box_top)
            if loyaties:
                loyaties[0].giftDate = None
                loyaties[0].giftTopOfCake = None
                loyaties[0].save()
        else:
            if  Adhesive.objects.filter(topOfCake=box_top).exists():
                adhesive = Adhesive.objects.get(topOfCake=box_top)
                loyatyCard = adhesive.loyatyCard
                loyatyCard_last = LoyatyCard.objects.filter(client=box_top.order.client).last()

                if loyatyCard != loyatyCard_last:
                     oldest_adhesive = Adhesive.objects.filter(loyatyCard=loyatyCard_last).first()
                     oldest_adhesive.loyatyCard = adhesive.loyatyCard
                     oldest_adhesive.save()
                     loyatyCard_last.finishedAt = None
                     loyatyCard_last.adhesiveCount -= 1;
                     loyatyCard_last.save()
                     if not Adhesive.objects.filter(loyatyCard=loyatyCard_last):
                         loyatyCard_last.delete()
                else:
                    loyatyCard.finishedAt = None
                    loyatyCard.adhesiveCount -= 1;
                    loyatyCard.save()
                adhesive.delete()
        box_top.order.totalOrder -= box_top.amount
        box_top.order.save()
        box_top.order.client.balance -= box_top.amount
        box_top.order.client.save()
        box_top.delete()
        return redirect(reverse('order_control:order_destroy', args=(box_top.order.id,)))


@login_required(login_url=reverse_lazy('order_control:login'))
def order_payment(request, id):
    form_submitted = False
    order = Order.objects.get(id=id)
    payments = Payment.objects.filter(order=order).order_by('createAt')
    if request.method == 'GET':
        form = PaymentForm()
        return render(request, 'order_control/order/payment.html',
                      {'order': order,'client': order.client, 'form': form, 'payments': payments, 'form_submitted': form_submitted})
    else:
        form_submitted = True
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.save()
            order.totalPayment += payment.amount
            order.client.balance -= payment.amount
            order.client.save()
            if payment.downPayment:
                order.downPayment += payment.amount
            order.save()
            order_form = OrderForm(instance=order)
            items_order = BoxTop.objects.filter(order=order)
            return render(request, 'order_control/order/update.html',
                {'order': order, 'form': order_form, 'items_order': items_order, 'form_submitted': form_submitted})


@login_required(login_url=reverse_lazy('order_control:login'))
def payment_destroy(request, id):
    payment = Payment.objects.get(id=id)
    form_submitted = False
    order = Order.objects.get(id=payment.order.id)
    if request.method == 'GET':
        form = PaymentForm(instance=payment)
        return render(request, 'order_control/order/destroy_payments.html', {'payment': payment, 'form': form})
    else:
        order.totalPayment -= payment.amount
        order.client.balance += payment.amount
        order.client.save()
        if payment.downPayment:
            order.downPayment -= payment.amount
        order.save()
        payment.delete()
        payments = Payment.objects.filter(order=order).order_by('createAt')
        form = PaymentForm()
        return render(request, 'order_control/order/payment.html',
                      {'order': order, 'client': order.client, 'form': form, 'payments': payments,
                       'form_submitted': form_submitted})


@login_required(login_url=reverse_lazy('order_control:login'))
def loyatyCard_details(request, id):
    loyatyCard = LoyatyCard.objects.get(id=id)
    adhesives = Adhesive.objects.filter(loyatyCard=loyatyCard)
    return render(request, 'order_control/order/loyatyCard_details.html', {'loyatyCard': loyatyCard, 'adhesives':adhesives})


def loyatyCard_update(request, id):
    isDelivered = request.POST.get('message').capitalize()
    loyatyCard = LoyatyCard.objects.get(id=id)
    loyatyCard.isDelivered = isDelivered
    loyatyCard.save()
    message = {"message": 'sucesso'}
    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )


class PurchaseView(LoginRequiredMixin, TemplateView):
    template_name = 'order_control/purchase/create.html'


class PurchaseListView(LoginRequiredMixin, TemplateView):
    template_name = 'order_control/purchase/list.html'


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'maxPage':  settings.REST_FRAMEWORK['PAGE_SIZE'],
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })

