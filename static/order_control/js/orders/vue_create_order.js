let data = new Date();

var vm = new Vue
({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        clients: [],
        avatar: "clients/noAvatar.png",
        noImage: "",
        artPreview: "boxes/noImage.png",
        totalOrder: 0,
        itemsQuantity: 0,
        client: 0,
        deliveryAt: data.getFullYear() + "-" + ("0" + (data.getMonth() + 1)).slice(-2) + "-" + ("0" + (data.getDate()) ).slice(-2),
        resetDate: data.getFullYear() + "-" + ("0" + (data.getMonth() + 1)).slice(-2) + "-" + ("0" + (data.getDate()) ).slice(-2),
        delivered: false,
        description : null,
        type: '',
        theme: null,
        birthdayName: null,
        amount: null,
        gift: false,
        wasGiftInGrid: false,
        message_gift_feed_back: '',
        id_storedIn: null,
        storedIn: [],
        items: [],
        button: 'Incluir Item',
        info: null,
    },
    methods: {
        loadClients(clients){
            this.clients = clients;
        },
        selectedClient(client_id){
            this.client = client_id;
            this.message_gift_feed_back = "";
            if (clients[client_id].picture)
                this.avatar = clients[client_id].picture;
            else this.avatar = "clients/noAvatar.png";
        },
        loadMediaAddress(media){
            this.noImage = media + this.artPreview;
            this.artPreview = media + this.artPreview;
        },
        previewFiles(event) {
            this.id_storedIn = event.target.files[0] || event.srcElement.files[0];
            if (!this.id_storedIn)
                this.artPreview = this.noImage;
            else if (this.id_storedIn)
                this.artPreview = window.URL.createObjectURL(this.id_storedIn);
        },
        isGift(){
            if (this.gift && this.client) {
                if (this.wasGiftInGrid || this.items.length > 0)
                    this.message_gift_feed_back = "Brinde deve ser o primeiro da lista!";
                else if ( this.type != "TOPPER")
                    this.message_gift_feed_back = "Só topos podem ser brindes";
                else {
                    axios.post("./eligible_gift/", this.client)
                    .then(response => {
                        if (response.data.eligible == 'False'){
                            this.message_gift_feed_back = "Cliente só possui " + response.data.adhesives_quantity + " adesivos";
                            this.gift = false;
                        }
                        else if (response.data.eligible == 'True' && this.clients.size > 0){
                            this.message_gift_feed_back = "Brinde só pode único na lista!!";
                            this.gift = false;

                        }
                        else {
                            this.amount = 0.00;
                            this.message_gift_feed_back = "";
                        }



                    })
                    .catch(error => {
                        console.log(error.response)
                    },
                    {
                        headers: {
                             'X-CSRFTOKEN': csrftoken,
                         },
                    });
                }
            } else if (!this.client && this.gift){
                this.message_gift_feed_back = "Selecione o cliente!!";
            }
        },
        formatPrice(value) {
            let val = (value/1).toFixed(2).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        },
        salveOrder () {
            if (this.items && this.client) {
                var data = {
                    "deliveryAt": new Date(this.deliveryAt),
                    "delivered": this.delivered,
                    "description": this.description,
                    "totalOrder": this.totalOrder,
                    "client": this.client,
                    "items": this.items,
                };


                 var formData = new FormData();

                 //dict of all elements


                formData.set("deliveryAt", new Date(this.deliveryAt).toISOString());
                formData.set("delivered", this.delivered);
                formData.set("description", this.description);
                formData.set("totalOrder", this.totalOrder);
                formData.set("client", this.client);
                formData.append("items", JSON.stringify(this.items));

                for (key in this.storedIn){
                    formData.append(this.storedIn[key]['name'], this.storedIn[key] )
                    }

                axios.post(
                    "../api/orders/",
                    formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                             headers: { 'X-CSRFTOKEN': csrftoken,}
                        }
                    }
                )
                .then(response => {
                  //  console.log(response['data']);

                    dict = response['data'];
                     stringResponseItem = "<ul>";
                     for(var key in dict) {
                         if (Array.isArray(dict[key]))
                            dict[key].forEach(function (item, indice, array) {
                                stringResponseItem += "<li>" ;
                                stringResponseItem += "Tipo: " + item['type'] + ", " ;
                                stringResponseItem += "Tema: " + item['theme'] + ", " ;
                                stringResponseItem += "Aniversariante: " + item['birthdayName'] + ", " ;
                                stringResponseItem += "Valor: " + item['amount'];
                                if (item['gift'])
                                    stringResponseItem += "Presente, "  ;
                                stringResponseItem += "</li>" ;
                                console.log("string: ", stringResponseItem);

                         });
                     }
                     stringResponseItem += "</ul>";

                     this.showToast("success","<div> Pedido criado com sucesso <br> " +
                                     "Id: <a href='../orders/" + JSON.stringify(response['data']['id']) + "/update/'>"  +
                                                      "<span class='label label-default' style='font-size:14px;' >" +
                                                       "<strong>" + JSON.stringify(response['data']['id']) + "</strong></span> </a> </br> " +
                                                        "Cliente: " + this.clients[response['data']['client']].name  + "<br>" +
                                                         stringResponseItem + "</div>" );

                    this.totalOrder = parseFloat(0);
                    this.itemsQuantity = 0;

                    this.theme = null;
                    this.birthdayName = null;
                    this.amount = 0;
                    this.gift = false;
                    this.client = 0;
                    this.items = [];
                    this.description = '';
                    $("#id_client ").val("0").change();
                    $("#id_storedIn").val('');
                    this.id_storedIn = null;
                    this.type = '';
                    this.message_gift_feed_back = '';
                    this.delivered = false;
                    this.deliveryAt = this.resetDate;
                    this.artPreview = this.noImage;

                })
                .catch(error => {
                    console.log(error.response);
                    this.showToast("error", "Erro --> " + error.response.request['response'])
                    }
                //, { headers: { 'X-CSRFTOKEN': csrftoken, }, }
                );
            }
        },
        formatPrice(value) {
            let val = (value/1).toFixed(2).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        },
        includeItem() {
            if (isNaN(this.amount))
                this.amount = this.amount.replace(',', '.');

            this.button !='Incluir Item' ? this.button = 'Incluir Item' : '';

            if (this.client){
                this.items.push({
                            "type": this.type,
                            "theme": this.theme,
                            "birthdayName": this.birthdayName,
                            "amount": this.amount,
                            "gift": this.gift,
                            "storedIn":  this.id_storedIn != null ? this.id_storedIn.name : null,



                })
                if (this.id_storedIn != null)
                    this.storedIn.push(this.id_storedIn)

                this.totalOrder += parseFloat(this.amount);
                this.itemsQuantity += 1;
                this.type = '';
                this.theme = null;
                this.birthdayName = null;
                this.amount = null;
                this.gift = false;
                $("#id_storedIn").val('');
                this.id_storedIn = null;

            }
        },
        excludeItem(keyItem){
            this.totalOrder -= parseFloat(this.items[keyItem].amount);
            this.storedIn.splice(keyItem, 1)
            this.$delete(this.items, keyItem);
            this.itemsQuantity -= 1;

        },
        editItem(keyItem){
            this.button=='Incluir Item' ? this.button = 'Editar Item' : '';
            this.totalOrder -= this.items[keyItem]['amount'];
            this.itemsQuantity -= 1;
            this.type = this.items[keyItem]['type'];
            this.theme = this.items[keyItem]['theme'];
            this.birthdayName = this.items[keyItem]['birthdayName'];
            this.amount = this.items[keyItem]['amount'];
            this.gift = this.items[keyItem]['gift'];
            this.id_storedIn = this.items[keyItem]['storedIn'];
            $("#id_storedIn").val(this.id_storedIn);

            this.$delete(this.items, keyItem);

        },
        toFormData(o) {
            return Object.entries(o).reduce((d,e) => (d.append(...e),d), new FormData())
        },
        showToast(method,response){
            toastr.options = {
            "closeButton": false,
            "debug": true,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-bottom-full-width",
            "preventDuplicates": false,
            "showDuration": "300",
            "hideDuration": "1000000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        }
        toastr[method](response);
        },
   },
})