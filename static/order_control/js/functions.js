let data = new Date();

// Carrega gráfico Inicial com dados do mês vigente
$(window).load(function() {
      $.ajax({
           "type": "POST",
            "dataType": "json",
            "url": "",
            "data": {'message': data.getFullYear() + '-' + ("0" + (data.getMonth() + 1)).slice(-2)},
            "success": function(message) {

                vm.vue_payments = groupByData(message.payments, 'client');
                vm.vue_payments =  _.orderBy(vm.vue_payments, 'amount', 'desc');
                drawChartPizza(vm.vue_payments);
                vm.vue_paymentsgroupByDateNoFilter = groupByData(message.payments, '');

                vm.vue_paymentsgroupByDate = groupByData(message.payments, 'date');
                vm.vue_purchasesgroupByDate = groupByDataPurchase(message.purchases);
                vm.vue_paymentsgroupByDate =  _.orderBy(vm.vue_paymentsgroupByDate, 'createAt', 'asc');


                drawChartLines(vueObjectToArrayLine(vm.vue_paymentsgroupByDate, vm.vue_purchasesgroupByDate));

                vm.vue_totalMensal = totalMensalCalc(vm.vue_payments);
                vm.vue_despesasTotal =  DespesatotalMensalCalc(vm.vue_purchasesgroupByDate);
            },
     });
});

function totalMensalCalc(payments){
    total = 0;
    payments.forEach(function(payment) {
        total += payment.amount;
    })
    return total;
}

function DespesatotalMensalCalc(purchases){
    total = 0;
    purchases.forEach(function(purchase) {
        total += purchase.amount;
    })
    return total;
}

//Agrupa dados em pagamentos por item "groupBy"
function groupByData(paymentList, groupBy){
   Payments = [];
   var repeated = false;
   paymentList.forEach(function(payment, idItem){

        if (groupBy == 'client')
            Payments.forEach(function(paymentJs, id) {
                if (paymentJs.client.id == payment['order__client__id']){
                    repeated = true;
                    Payments[id].amount = parseFloat(Payments[id].amount) + parseFloat(payment['amount']);
                    return;
                }
            })

        if (groupBy == 'date')
             Payments.forEach(function(paymentJs, id) {
                if (paymentJs.createAt == payment['createAt']){
                    repeated = true;
                    Payments[id].amount = parseFloat(Payments[id].amount) + parseFloat(payment['amount']);
                    return;
                }
            })


        if (!repeated){
            client = new Client(payment['order__client__id'], payment['order__client__name'],
            payment['order__client__cakeMaker'], payment['order__client__balance'],
            payment['order__client__id']);

            payment = new Payment(payment['id'], payment['type'], payment['createAt'],
            parseFloat(payment['amount']), client);
            Payments.push(payment);
            repeated = false;
        }
        else repeated = false;
    })
    return Payments
}

//Agrupa dados em compras por item "groupBy"
function groupByDataPurchase(purchaseList){
   Purchases = [];
   var repeated = false;
   purchaseList.forEach(function(purchase, idItem){
       Purchases.forEach(function(purchaseJs, id) {
            if (purchaseJs.createAt == purchase['createAt']){
                repeated = true;
                Purchases[id].amount = parseFloat(Purchases[id].amount) + parseFloat(purchase['amount']);
                return;
            }
       })

       if (!repeated){
            purchase = new Purchase(purchase['id'], purchase['createAt'], parseFloat(purchase['amount']));
            Purchases.push(purchase);
       } else repeated = false;
    })
    return Purchases
}


function vueObjectToArrayPizza(o){
    array = [];
    array.push(['Cliente', 'Valor']);
    for (key in o)
        array.push([o[key].client.name , parseFloat(o[key].amount)]);
    return array;
}

function vueObjectToArrayLine(order, purchase){
    array = [];
    var repeated = false;

    // insere em um array [data, valor pedido, valor compra] todos os pedidos
    // valores de compra nulos
    var totalCrescentePorDia = 0;
    for (key in order){
        totalCrescentePorDia =  totalCrescentePorDia + parseInt(order[key].amount);
        array.push([ order[key].createAt.substring(8, 10) , totalCrescentePorDia, null]);
    }

    // insere todos as compras
    // caso ja tenha a mesma data no array altera somente o valor da compra que era nulo
    // caso não tenha insere novo item no array e poe valor do pedido nulo
    for (key in purchase){
        array.forEach(function(itemArray, id){
            if (itemArray[0] == purchase[key].createAt.substring(8, 10)){
                array[id][2] = purchase[key].amount;
                repeated = true;
            }
        })
        if (!repeated)
            array.push([ purchase[key].createAt.substring(8, 10) , null, purchase[key].amount]);
        else repeated = false;

    }

    // colocando em ordem crescente e preenchendo os campos nulos do array
    // caso seja campo nulo preencha com o valor anterior
    // caso seja o primeiro e nulo preencha com zero
    // soma o item anterior com o atual
    array.sort(function (a, b) {
        return a[0] - b[0];
    });
    totalCrescentePorDia = 0;
    array.forEach(function(value, id){
        if (value[1] == null && id > 0)
            array[id][1] = array[id -1][1];
        else if (value[1] == null && id == 0)
            array[id][1] = 0

        if (value[2] != null){
            totalCrescentePorDia += array[id][2];
            array[id][2] = totalCrescentePorDia;
        }
        if (value[2] == null && id > 0)
            array[id][2] = totalCrescentePorDia;
        else if (value[2] == null && id == 0)
            array[id][2] = 0
    })
    array.unshift(['Dia', 'Arrecadação', 'Gastos']);
    return array;
}


// Gráfico Google tipo pizza

google.charts.load('current', {'packages':['corechart']});
//google.charts.setOnLoadCallback(drawChartPizza);
//google.charts.setOnLoadCallback(drawChartLines);

function drawChartPizza(dataToGraphsPizza) {
    var data = google.visualization.arrayToDataTable(vueObjectToArrayPizza(dataToGraphsPizza));

    var options = {
      title: 'Clientes x Arrecadação Mensal',
      is3D: true,
    };

    var chart = new google.visualization.PieChart(document.getElementById('chartPizza'));
    chart.draw(data, options);
}

function drawChartLines(dataToGraphsLines) {
    var data = google.visualization.arrayToDataTable(dataToGraphsLines);

    var options = {
      title: 'Arrecadação por dias do Mês',
      curveType: 'function',
      legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}