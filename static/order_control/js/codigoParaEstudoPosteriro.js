var dict = {
     deliveryAt: '2021-12-24T00:00:00.000Z',
     delivered: false,
     description: null,
     totalOrder: 67,
     client: 31
};

 	 dict.items = [
		{
		 type: 'TOPPER',
		 theme: 'Homem Aranha',
		 birthdayName: 'Piter Park',
		 amount: 35,
		 gift: false,
		 image: null
		},
		{
		 type: 'TOPPER',
		 theme: 'Master Class',
		 birthdayName: 'Antony JavaScript Junior',
		 amount: 32,
		 gift: false,
		 image: null
		}
		]

        for(var key in dict) {
            // o if abaixo verifica se é um array e na estrutura acima temos um array em dict.items
            // caso seja ele entra no forEach e
            // dessa forma ele percorre cada elemento do array dict.items,
            if (Array.isArray(dict[key]))
                dict[key].forEach(function (item, indice, array) {
                    console.log("item: ", indice, " -> " ,item);
                });
            else
                console.log(key + ": " + dict[key]);
        }


   JsonToDictObject = JSON.parse(json);

// axios.post - estabelecemos o verbo rest, neste caso post
// "../api/orders/" - o endereço no servidor que irá receber a resquisição
// dictToJson, - os dados a serem envidados.


axios.post(
    "../api/orders/",
    formData,
    { headers: {
            'Content-Type': 'multipart/form-data',
             headers: { 'X-CSRFTOKEN': csrftoken, } }
    }
)
.then(response => {
    console.log(response)
})
.catch(error => { console.log(error.response)  },
);

