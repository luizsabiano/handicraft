
let meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro' ]
var teste = null;
var vm = new Vue ({
    delimiters: ["[[", "]]"],
    el: "#app",
    data: {
        months: meses,
        monthSelected: meses[data.getMonth()],
        years: [2021, 2022, 2023, 2024, 2025, 2026, 2026, 2028, 2029, 2030],
        yearSelected: data.getFullYear(),
        vue_payments: 0,
        vue_purchases: 0,
        vue_paymentsgroupByDate: 0,
        vue_paymentsgroupByDateNoFilter: 0,
        vue_purchasesgroupByDateNoFilter: 0,
        vue_totalMensal: 0,
        vue_despesasTotal:0,
        isChecked: false,
        loyatyCard: {
            total: 0,
            client: 0,
            client_name: "luiz sabiano",
        },
        ordem: {
          colunas: ['amount'],
          orientacao: ['desc']
        }
    },
    methods: {
       onChange(event) {
             $.ajax({
               "type": "POST",
                "dataType": "json",
                "url": "",
                "data": {'message': event.target.value},
                "success": function(message) {
                    vm.isChecked = false;
                    vm.vue_payments = groupByData(message.payments, 'client');
                    vm.vue_payments =  _.orderBy(vm.vue_payments, 'amount', 'desc');
                    drawChartPizza(vm.vue_payments);
                    vm.vue_paymentsgroupByDateNoFilter = groupByData(message.payments, '');

                    vm.vue_paymentsgroupByDate = groupByData(message.payments, 'date');
                    vm.vue_purchasesgroupByDate = groupByDataPurchase(message.purchases);
                    vm.vue_paymentsgroupByDate =  _.orderBy(vm.vue_paymentsgroupByDate, 'createAt', 'asc');

                    vm.vue_totalMensal = totalMensalCalc(vm.vue_payments);
                    vm.vue_despesasTotal =  DespesatotalMensalCalc(vm.vue_purchasesgroupByDate);
                },
             });
       },
       onChangeCheckbox(event){
            var payments = vm.vue_payments;

            if (this.isChecked)
                payments = _.filter(payments, ['client.cakeMaker', true ]);
            vm.vue_totalMensal = totalMensalCalc(payments);
            drawChartPizza(payments);

            if (this.isChecked){
                paymentsGroupByDate = _.filter(vm.vue_paymentsgroupByDateNoFilter, ['client.cakeMaker', true ]);
                paymentsGroupByDate = groupByData(paymentsGroupByDate, 'date');
                paymentsGroupByDate = _.orderBy(paymentsGroupByDate, 'createAt', 'asc');
            }
            else
                paymentsGroupByDate = vm.vue_paymentsgroupByDate;
       }
    },
})



