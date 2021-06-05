from django.shortcuts import render, reverse, redirect

from order_control.form import ClientForm
from order_control.models import Client


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