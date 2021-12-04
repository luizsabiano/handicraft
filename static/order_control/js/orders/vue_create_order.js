let data = new Date();

var vm = new Vue
({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        orderAmount: 0,
        totalItens: 0,

        quantity: null,
        amount: null,
        itemsQuantity: 0,
        createAt: data.getFullYear() + "-" + ("0" + (data.getMonth() + 1)).slice(-2) + "-" + ("0" + data.getDate()).slice(-2),
        items: [],
        button: 'Incluir Item',
        info: null,
    },
    methods: {
        includeItem() {
            if (isNaN(this.amount))
                this.amount = this.amount.replace(',', '.');

            this.button !='Incluir Item' ? this.button = 'Incluir Item' : '';
            this.itemsQuantity += 1;

            this.items.push({
                        "name": this.product,
                        "quantity": this.quantity,
                        "amount": this.amount
                        })

            this.purchaseAmount += parseFloat(this.amount);

            this.product = '';
            this.quantity = null;
            this.amount = null;
        },
        excludeItem(keyItem){
            this.purchaseAmount -= parseFloat(this.items[keyItem].amount);
            this.$delete(this.items, keyItem);
        },
        editItem(keyItem){
            this.button=='Incluir Item' ? this.button = 'Editar Item' : '';
            this.product = this.items[keyItem]['name'];
            this.quantity = this.items[keyItem]['quantity'];
            this.amount = this.items[keyItem]['amount'];
            this.$delete(this.items, keyItem);
            this.purchaseAmount -= parseFloat(this.amount);
        },
        salve () {
          var data = {
            "createAt": this.createAt,
            "amount": this.purchaseAmount.toString()
          };


         // message.items = JSON.parse(this.items);
          data.items = this.items;
          console.log('array: ', data);

          axios.post("../api/purchases/", data)
            .then(response => {
                console.log(response)
                this.product = '';
                this.quantity = null;
                this.amount = null;
                this.purchaseAmount = null;
                this.items = [];
                this.createAt = data.getFullYear() + "-" + ("0" + (data.getMonth() + 1)).slice(-2) + "-" + ("0" + data.getDate()).slice(-2)
            })
            .catch(error => {
                console.log(error.response)
            },
            {
                headers: {
                     'X-CSRFTOKEN': csrftoken,
                 },
            },
            );
        },
   },
})