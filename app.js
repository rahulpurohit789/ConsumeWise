const express = require('express');
const axios = require('axios');
const { exec } = require('child_process');
const WebSocket = require('ws');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

const wss = new WebSocket.Server({ noServer: true });

wss.on('connection', (ws) => {
    console.log('WebSocket connection established.');

    ws.on('message', async (message) => {
        try {
            // Parse JSON data from the WebSocket message
            const { barcode } = JSON.parse(message);

            console.log('Received barcode:', barcode);
            await handleBarcode(barcode, ws);
        } catch (error) {
            console.error('Error parsing message:', error);
            ws.send(JSON.stringify({ error: 'Invalid message format' }));
        }
    });

    ws.on('close', () => {
        console.log('WebSocket connection closed.');
    });
});

async function handleBarcode(barcode, ws) {
    const countryCode = 'in';
    const url = `https://${countryCode}.openfoodfacts.org/api/v0/product/${barcode}.json`;

    try {
        const response = await axios.get(url);
        const product = response.data.product;

        if (product) {
            const productName = product.product_name || 'Unknown Product';
            const brandName = product.brands || 'Unknown Brand';
            const combinedName = `${brandName} ${productName}`.trim();

            console.log(`Product Name: ${productName}, Brand: ${brandName}`);

            exec(`python llama_inference.py "${combinedName}"`, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing LLaMA script: ${stderr}`);
                    ws.send(JSON.stringify({ error: 'Error generating response' }));
                    return;
                }

                console.log('LLaMA Output:', stdout);
                ws.send(stdout.trim());
            });
        } else {
            console.log('Product not found');
            ws.send(JSON.stringify({ error: 'Product not found' }));
        }
    } catch (error) {
        console.error('Error fetching product data:', error);
        ws.send(JSON.stringify({ error: 'Error fetching product data' }));
    }
}

const server = app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

server.on('upgrade', (request, socket, head) => {
    wss.handleUpgrade(request, socket, head, (ws) => {
        wss.emit('connection', ws, request);
    });
});
