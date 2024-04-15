import {connect} from './node_modules/nats.ws/esm/nats.js';

class Nats {
    constructor() {
        this.connection = null;
    }

    async connect() {
        try {
            this.connection = await connect({servers: "ws://localhost:9222"});
            console.log("Connected to NATS server");
        } catch (error) {
            console.error("Error:", error);
        }
    }
}

const nats = new Nats();

nats.connect();


const publishButton = document.getElementById('updatePriceButton');
publishButton.addEventListener('click', updatePrice);

async function updatePrice() {
    const priceText = document.getElementById("priceText");
    const coinName = document.getElementById("coinName").value;

    let rep = await nats.connection.request(
        "crypto.price",
        coinName,
    );
    priceText.innerHTML = rep.string();
}
