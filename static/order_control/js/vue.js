Payments2 = []

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
        vue_payments: '',
        vue_totalMensal : '',
        ordem: {
          colunas: ['amount'],
          orientacao: ['desc']
        }
    },
    methods: {
       onChange(event) {
       var vm = this;
       console.log('mensagem evento: ', event.target.value)
         $.ajax({
           "type": "POST",
            "dataType": "json",
            "url": "",
            "data": {'message': event.target.value},
            "success": function(message) {

                this.vue_payments = groupByData(message.payments, 'client');
                this.vue_payments =  _.orderBy(this.vue_payments, 'amount', 'desc');
                drawChart(this.vue_payments);
                vm.vue_totalMensal = message.totalPayments.amount__sum;
            },
         });
       }
    },
})

function vueObjectToArray(o){
    array = [];
    array.push(['Cliente', 'Valor']);
    for (key in o){
        array.push([o[key].client.name , parseFloat(o[key].amount)]);
    }
    return array;
}