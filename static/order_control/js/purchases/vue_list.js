var vm = new Vue
({
    delimiters : ['[[', ']]'],
    el: '#app',
    data: {
        purchases: [],
        pagination: {
            next: null,
            previous: null,
            count: 0,
            current: 1,
            maxPage: 10,
        },


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
                vm.purchases.splice(arraykey,1);
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
                vm.purchases[keyArray]['items'].splice(keyItem,1);
                vm.purchases[keyArray]['amount'] = parseFloat(vm.purchases[keyArray]['amount']) - parseFloat(response['data']['amount']);
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
        listPurchasePagination(url){
            $.ajax({
           "type": "GET",
            "dataType": "json",
            "url": url,
            "success": function(message) {
                vm.purchases = message['results'];
                vm.pagination.next = message['next'];
                vm.pagination.previous = message['previous'];
                vm.pagination.count = Math.ceil(parseFloat(message['count'])/ vm.pagination.maxPage);
                if (message['next'])
                    vm.pagination.current = parseInt(message['next'].split("page=")[1]) - 1;
                else vm.pagination.current = null;
            },
     });
        },
    },
})