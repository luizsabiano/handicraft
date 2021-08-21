const event = new Vue();


var navPagination = Vue.extend({
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


// Tentativa de retirar variável global
// Funciona para integrar com modulos, porem tentei em componentes.
// Vue.use(navPagination);
// Erro: Cannot read property '_init' of null

var vm = new Vue
({
    delimiters : ['[[', ']]'],
    el: '#app',
    data: {
        list: [],
    },
    components: {
        'nav-pagination': navPagination,
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

