let data = new Date();

// Carrega gráfico Inicial com dados do mês vigente
$(window).load(function() {
      $.ajax({
           "type": "POST",
            "dataType": "json",
            "url": "",
            "data": {'message': data.getFullYear() + '-' + (parseInt(data.getMonth()) + 1)},
            "success": function(message) {

                vm.vue_payments = groupByData(message.payments, 'client');
                vm.vue_payments =  _.orderBy(vm.vue_payments, 'amount', 'desc');
                drawChartPizza(vm.vue_payments);

                vm.vue_paymentsgroupByDateNoFilter = groupByData(message.payments, '');
                //vm.vue_purchasesgroupByDateNoFilter = groupByDataPurchase(message.purchases);

                vm.vue_paymentsgroupByDate = groupByData(message.payments, 'date');
                vm.vue_purchasesgroupByDate = groupByDataPurchase(message.purchases);
                vm.vue_paymentsgroupByDate =  _.orderBy(vm.vue_paymentsgroupByDate, 'createAt', 'asc');


                drawChartLines(vm.vue_paymentsgroupByDate, vm.vue_purchasesgroupByDate);

                vm.vue_totalMensal = totalMensalCalc(vm.vue_payments);
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
            repeated = true;
            if (purchaseJs.createAt == purchase['createAt']){
                repeated = true;
                Purchases[id].amount = parseFloat(Purchases[id].amount) + parseFloat(purchase['amount']);
                return;
            }
       })

       if (!repeated){
            purchase = new Purchase(purchase['id'], purchase['createAt'], parseFloat(purchase['amount']));
            Purchases.push(purchase);
            repeated = false;
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

function vueObjectToArrayLine(o, lines){
    array = [];
    array.push(['Dia', 'Arrecadação', 'Gastos']);
    totalCrescentePorDia = 0;
    for (key in o){
        totalCrescentePorDia =  totalCrescentePorDia + parseInt(o[key].amount);
        array.push([ o[key].createAt.substring(8, 10) , totalCrescentePorDia, 0]);
    }

    for (key in lines){
        array.forEach(function(purchase, id){
            if (purchase[0] == lines[key].createAt.substring(8, 10)){
                array[id][2] = lines[key].amount;
                totalCrescentePorDia = array[id][1];
                return;
            }
        })

        array.push([ lines[key].createAt.substring(8, 10) , totalCrescentePorDia, lines[key].amount]);
    }
    console.log(array)
    return array;
}


// Gráfico Google tipo pizza

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChartPizza);
google.charts.setOnLoadCallback(drawChartLines);

function drawChartPizza(dataToGraphsPizza) {
    var data = google.visualization.arrayToDataTable(vueObjectToArrayPizza(dataToGraphsPizza));

    var options = {
      title: 'Clientes x Arrecadação Mensal',
      is3D: true,
    };

    var chart = new google.visualization.PieChart(document.getElementById('chartPizza'));
    chart.draw(data, options);
}

function drawChartLines(dataToGraphsPizza, dataToGraphsLines) {
    var data = google.visualization.arrayToDataTable(vueObjectToArrayLine(dataToGraphsPizza, dataToGraphsLines));

    var options = {
      title: 'Arrecadação por dias do Mês',
      curveType: 'function',
      legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}