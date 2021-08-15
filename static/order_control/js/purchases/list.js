
$(window).load(function() {
      $.ajax({
           "type": "GET",
            "dataType": "json",
            "url": "../api/purchases/",
            "success": function(message) {
                vm.purchases = message['results'];
                vm.pagination.next = message['next'];
                vm.pagination.previous = message['previous'];
                vm.pagination.count = Math.ceil(parseFloat(message['count'])/ vm.pagination.maxPage);
            },
     });
});