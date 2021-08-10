let data = new Date();

var vm = new Vue
({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        purchaseAmount: 0,
        product: '',
        quantity: null,
        amount: null,
        itemsQuantity: 0,
        items: {},
        button: 'Incluir Item',
        info: null,
    },
    methods: {
        includeItem() {
            if (isNaN(this.amount))
                this.amount = this.amount.replace(',', '.');

            this.button !='Incluir Item' ? this.button = 'Incluir Item' : '';
            this.itemsQuantity += 1;
            Vue.set(this.items, 'item' + this.itemsQuantity,
                        {
                        "name": this.product,
                        "quantity": parseInt(this.quantity),
                        "amount": parseFloat(this.amount),
                        "purchase": ""
                        }
            );

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
          var message = {};
          message.purchases = {
            "createAt": data.getFullYear() + "-" + data.getMonth() + "-" + data.getDay(),
            "amount": this.purchaseAmount
          };


          message.items = this.items;
          console.log(message);

          axios.post("http://127.0.0.1:8000/api/purchases/", message)
            .then(response => {
                console.log(response)
                this.product = '';
                this.quantity = null;
                this.amount = null;
                this.purchaseAmount = null;
                this.items = {};
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