// variável global criada pq o child não reconhecia uma variável
// parent, aparentemente o component filho é criado antes do pai
// logo, a variavel pai nao existe no momento da atribuição.
var list;

var navPagination = Vue.extend({
    delimiters : ['[[', ']]'],
    props: ['postTitle'],
    data: function() {
        return {
            next: localStorage.getItem('next'),
            previous: null,
            count: localStorage.getItem('count'),
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
        this.listPurchasePagination('../api/purchases/');
    },
    methods: {
        listPurchasePagination(url){
            var pagination;
            $.ajax({
                "type": "GET",
                "dataType": "json",
                "url": url,
                "success": function(message) {
                    list = message['results'];
                    next = null;
                    previous = null;
                    current = null;
                    if (message['next'])
                        next = message['next'];
                    if (message['previous'])
                        this.previous = message['previous'];
                    if (message['next'])
                        current = parseInt(message['next'].split("page=")[1]) - 1;

                    count = Math.ceil(parseFloat(message['count'])/ message['maxPage']);
                    pagination = {'next': message['next'], 'previous': message['previous'], 'count': count, 'current': current, 'list': list};
                },
                async: false,
            })
            this.next = pagination['next'];
            this.previous = pagination['previous'];
            this.count = pagination['count'];
            this.current = pagination['current'];
            if (vm){
                vm.list = pagination['list'];
                list = null;
            }

        },

    },
});


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
        this.list = list
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
    },

});

