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
                drawChart(vm.vue_payments);
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

//Agrupa dados por item "groupBy"
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

        if (!repeated){
            client = new Client(payment['order__client__id'], payment['order__client__name'],
            payment['order__client__cakeMaker'], payment['order__client__balance'],
            payment['order__client__id']);

            payment = new Payment(payment['id'], payment['type'], payment['createAt'],
            parseFloat(payment['amount']), client);
            Payments.push(payment);
            repeated = false;
        }
        else{
            repeated = false;

        }
    })
    return Payments
}



// Gráfico Google tipo pizza

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart(dataToGraphs) {
    var data = google.visualization.arrayToDataTable(vueObjectToArray(dataToGraphs));

    var options = {
      title: 'Clientes x Arrecadação Mensal',
      is3D: true,
      //pieHole: 0.4,
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
}