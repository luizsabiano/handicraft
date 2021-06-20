$(function(){

    // Carrega Jogo
    $(window).load(function() {
     // faça algo quando carregar
     $("#ItemCreate").hide();
    });

    // Envia Dados e Recebe Dados do servidor
    // Chama funcoes de acordo com a resposta do servidor
    function sendajax(Dados, Url){
        $.ajax({
                "type": "POST",
                "dataType": "json",
                "url": Url,
                "data": Dados,
                "success": function(message) {
                /// $('#itemsOrder tr:last').after('<tr> <td>' + message['order_control.boxtop']['type'] +'</td> <td>Tema</td><td>Aniversariante</td><td>Valor</td><td><a href="">Editar<a> | <a href="">Excluir<a> </td> </tr>');
                dados = JSON.parse(message['top_box']);
                createTableJson(dados);
                },
         });
    }

    function createTableJson(dados){
        headTable = '<table class="table table-striped table-hover" id="itemsOrder"> <thead> <tr style="color: #fff; background: black;"> <th>Tipo</th> <th>TEMA</th> <th>ANIVERSARIANTE</th> <th>VALOR</th> <th>AÇÕES</th> </tr> </thead> <tbody> ';
        fotterTable = '</tbody> </table>';
        bodyTable = '';
        this.totalOrder = 0;
        for ( i = 0; i < dados.length; i++){
            pk = dados[i]['pk'];
            tipo = dados[i]['fields']['type'];
            tema = dados[i]['fields']['theme'];
            aniversariante = dados[i]['fields']['birthdayName'];
            valor = dados[i]['fields']['amount'];
            this.totalOrder = parseFloat(this.totalOrder) + parseFloat(valor);
            bodyTable =  bodyTable + '<tr> <th>'+ tipo + '</th> <th>'+ tema + '</th> <th>'+ aniversariante + '</th> <th>'+
            valor + '</th> <th><a href="../../items/'+ pk +'/update/">Editar<a> | <a href="../../items/'+ pk +'/destroy/">Excluir<a></th> </tr>';
        }
        $("#divTableItems").html(headTable + bodyTable + fotterTable)
        $("#totalOrder").html(this.totalOrder.toFixed(2))
        }



    // this is the id of the form
    $('#teste').submit(function () {
        event.preventDefault();
        this.form = $(this);
        this.url = this.form.attr('action');
        this.dados = this.form.serialize();
        sendajax(this.dados,this.url);
    });

    $("#showItemCreate").click(function(){
        $("#hideDescription").hide();
        $("#ItemCreate").show();

        // Limpa os campos adição de itens
        $('#id_theme').val("");
        $('#id_birthdayName').val("");
        $('#id_description').val("");
        $('#id_amount').val("");
        $('#id_type').val("TOPO")
        $("#id_storedIn").val(null);

        // $(".childNode").hide(100);
        //$(this).children().show(100);
    });

    $("#caixaBoxCreate").click(function(){
        $("#hideDescription").show();
        $("#ItemCreate").hide();
    });

    $("#caixaBoxCreate2").click(function(){
        $("#hideDescription").show();
        $("#ItemCreate").hide();
    });


});