const event = new Vue();

Vue.component('my-app', {
    props: ['list'],
    delimiters : ['[[', ']]'],
    template: `
        <div class="container">
            <br/>
            <div class="row">
                <div class="col"><h1>Lista de Compras</h1></div>
                <div class="col">
                    <!-- navPagination -->
                    <nav-pagination></nav-pagination>
                </div>
            </div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>
                            <div class="row">
                                <div class="col-md-3">Data</div>
                                <div class="col-md-3">Valor</div>
                                <div class="col-md-2">Quant. Items</div>
                                <div class="col-md-2">Acões</div>
                            </div>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(purchase, key) in list">
                        <td>
                            <div class="row">
                                <div class="col-md-3">[[purchase['createAt'] ]]</div>
                                <div class="col-md-3">[[purchase['amount'] ]]</div>
                                <div class="col-md-2">[[purchase['items'].length ]]</div>
                                <div class="col-md-2"><a href="#" @click.prevent="showItems(key)">Editar </a> | <a href="#" @click="excludePurchase([[purchase['id'] ]], key)">Excluir</a></div>
                            </div>
                            <div  :id="key" class="card" v-show="false">
                                <br>
                                <div class="col">
                                <table class="table table-sm">
                                    <tbody>
                                        <tr v-for="(item, keyItem) in purchase['items']">
                                            <td>[[ item['name'] ]]</td>
                                            <td>[[ item['quantity'] ]]</td>
                                            <td>[[ item['amount'] ]]</td>
                                            <td><a href="#" @click="excludeItemsPurchase([[ item['id'] ]], key, keyItem)">Excluir</a></td>
                                        </tr>
                                    </tbody>
                                </table>
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>

            </table>
        </div>
    `
});


Vue.component('nav-pagination', {
    delimiters : ['[[', ']]'],
    data: function() {
        return {
            next: null,
            previous: null,
            count: 1,
            current: 1,
        }
    },
    /* `` uso da crase é permitido desde o EMA Script 6 possibilitando
          o código html ( template ) seja multilinha */
    template: `
        <nav aria-label="...">
          <ul class="pagination">
            <li class="page-item disabled">
              <a class="page-link" href="#" tabindex="-1">Página [[ current ? current : count ]] de [[ count ]]</a>
            </li>
            <li :class="previous ? 'page-item' : 'page-item disabled'">
              <a class="page-link" href="#" @click="listPurchasePagination(previous)"> Anterior</a>
            </li>
            <li :class="next ? 'page-item' : 'page-item disabled'">
              <a class="page-link" href="#" @click="listPurchasePagination(next)"> Próxima</a>
            </li>
          </ul>
        </nav>
    `,
    mounted: function(){
        event.$on('get-pagination', (pagination) => {
            current = null;
            if (pagination['next'])
                current = parseInt(pagination['next'].split("page=")[1]) - 1;

            count = Math.ceil(parseFloat(pagination['count'])/ pagination['maxPage']);
            this.next = pagination['next'];
            this.previous = pagination['previous'];
            this.count = count;
            this.current = current;
        });

    },
    methods: {
        listPurchasePagination(url){
            event.$emit('get-list', url);
        },

    },
});


var vm = new Vue
({
    template: '<my-app :list="list"></my-app>',
    delimiters : ['[[', ']]'],
    el: '#app',
    data: {
        list: [],
    },
    mounted: function(){
       this.getList('../api/purchases/');

       event.$on('get-list', (url) => {
            this.getList(url);
        });

    },
    methods: {
        showItems(key) {
            var x = document.getElementById(key);
            if (x.style.display === "none") {
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }
        },
        excludePurchase(id, arraykey) {
          axios.delete("../api/purchases/" + id)
            .then(response => {
                this.list.splice(arraykey,1);
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
        excludeItemsPurchase(id, keyArray, keyItem) {
          axios.delete("../api/purchasesItems/" + id)
            .then(response => {
                this.list[keyArray]['items'].splice(keyItem,1);
                this.list[keyArray]['amount'] = parseFloat(this.list[keyArray]['amount']) - parseFloat(response['data']['amount']);
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
        getList(url){
            $.ajax({
                "type": "GET",
                "dataType": "json",
                "url": url,
                "success": function(message) {
                    vm.list = message['results'];
                    // paginação
                    pagination = {'next': message['next'], 'previous': message['previous'], 'count': message['count'], 'maxPage': message['maxPage'] };
                    event.$emit('get-pagination', pagination);
                }
            });
        },
    },

});

