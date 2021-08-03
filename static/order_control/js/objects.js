class Client {
    constructor(id, name, cakeMaker, balance, url_detail){
        this.id = id;
        this.name = name;
        this.cakeMaker = cakeMaker;
        this.balance = balance;
        this.url_detail = url_detail;
    }
    }

    class Payment {
        constructor(id, type, createAt, amount, client){
            this.id = id;
            this.type = type;
            this.createAt = createAt;
            this.amount = amount;
            this.client = client;
    }
}