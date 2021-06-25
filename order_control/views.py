import json

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect
from django.utils import timezone
from django.views.generic import TemplateView, CreateView

from order_control.form import ClientForm, OrderForm,  BoxTopForm
from order_control.models import Client, Order, BoxTop, LoyatyCard, Adhesive


class LoginView(TemplateView):
    template_name = 'order_control/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            print(vars(user))
            django_login(request, user)
            return redirect('/')  # redirect é um atalho para HttpResponseRedirect
        message = 'Credenciais Inválidas'
        return self.render_to_response({'message': message})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'order_control/index.html'


class FormSubmittedIncontextMixin:

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, form_submitted=True))


class ClientCreateView(LoginRequiredMixin, FormSubmittedIncontextMixin, CreateView):
    model = Client
    #   fields = ['address', 'address_complement', 'city', 'state', 'country']
    form_class = ClientForm
    template_name = 'order_control/client/create.html'
    # para não entrar na página de detalhes e usar a list.
    # success_url = reverse_lazy('my_app:address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def client_create(request):
    form_submitted = False
    if request.method == 'GET':
        form = ClientForm()
    else:
        form_submitted = True
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect(reverse('order_control:client_list'))

    return render(request, 'order_control/client/create.html', {'form': form, 'form_submitted': form_submitted})


def client_update(request, id):
    form_submitted = False
    client = Client.objects.get(id=id)
    if request.method == 'GET':
        form = ClientForm(instance=client)
    else:
        form_submitted = True
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect(reverse('order_control:client_list'))

    return render(request, 'order_control/client/update.html',
                  {'client': client, 'form': form, 'form_submitted': form_submitted})


def client_destroy(request, id):
    client = Client.objects.get(id=id)
    if request.method == 'GET':
        form = ClientForm(instance=client)
    else:
        client.delete()
        return redirect(reverse('order_control:client_list'))

    return render(request, 'order_control/client/destroy.html', {'client': client, 'form': form})


def client_list(request):
    clients = Client.objects.all()
    print(list(clients))
    return render(request, 'order_control/client/list.html', {'clients': clients})


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
            if box_top.order.client.cakeMaker is True and box_top.type == "TOPO":
                if not LoyatyCard.objects.filter(client=box_top.order.client).exists():
                    LoyatyCard(client=box_top.order.client).save()
                else:
                    if LoyatyCard.objects.filter(client=box_top.order.client).last().finishedAt:
                        LoyatyCard(client=box_top.order.client).save()

                loyatyCard = LoyatyCard.objects.filter(client=box_top.order.client).last()
                adhesive = Adhesive(topOfCake=box_top, loyatyCard=loyatyCard)
                adhesive.save()
                print(Adhesive.objects.filter(loyatyCard=loyatyCard).count())
                if Adhesive.objects.filter(loyatyCard=loyatyCard).count() > 2:
                    loyatyCard.finishedAt = timezone.now()
                    loyatyCard.save()

            # Fechar cartao fidelidade com 10 adesivos
            box_top_json = serializers.serialize("json", BoxTop.objects.filter(order=box_top.order.id))
            message = {"top_box": box_top_json}
            return HttpResponse(
                json.dumps(message),
                content_type="application/json"
            )


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
            order.totalPayment = order.downPayment
            order.save()
            box_top_form = BoxTopForm()
            return render(request, 'order_control/order/order_add_items.html',
                          {'order': order, 'box_top_form': box_top_form, 'client': order.client, 'box_top': items_order })
    return render(request, 'order_control/order/update.html',
                  {'order': order, 'form': form, 'items_order': items_order, 'form_submitted': form_submitted})


def order_items_update(request, id):
    form_submitted = False
    box_top = BoxTop.objects.get(id=id)
    if request.method == 'GET':
        form = BoxTopForm(instance=box_top)
    else:
        form_submitted = True
        form = BoxTopForm(request.POST, request.FILES, instance=box_top)
        if form.is_valid():
            form.save()
            return redirect(reverse('order_control:order_update', args=(box_top.order.id,)))

    return render(request, 'order_control/order/update_items.html',
                  {'box_top_form': form, 'box_top': box_top, 'form_submitted': form_submitted})


def order_list(request):
    order = Order.objects.all().order_by('delivered', 'deliveryAt')
    return render(request, 'order_control/order/list.html', {'orders': order})


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


def order_items_destroy(request, id):
    box_top = BoxTop.objects.get(id=id)
    if request.method == 'GET':
        form = BoxTopForm(instance=box_top)
    else:
        adhesive = Adhesive.objects.get(topOfCake=box_top)
        if adhesive:
            loyatyCard = adhesive.loyatyCard
            loyatyCard_last = LoyatyCard.objects.filter(client=box_top.order.client).last()

            if loyatyCard != loyatyCard_last:
                 oldest_adhesive = Adhesive.objects.filter(loyatyCard=loyatyCard_last).first()
                 oldest_adhesive.loyatyCard = adhesive.loyatyCard
                 oldest_adhesive.save()
                 if not Adhesive.objects.filter(loyatyCard=loyatyCard_last):
                     loyatyCard_last.delete()
            else:
                loyatyCard.finishedAt = None

        loyatyCard.save()
        adhesive.delete()
        box_top.delete()
        return redirect(reverse('order_control:order_destroy', args=(box_top.order.id,)))

    return render(request, 'order_control/order/destroy_items.html', {'box_top': box_top, 'box_top_form':   form})
