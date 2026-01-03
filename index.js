const express = require('express');
const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => {
    res.send(`
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h1 style="text-align:center;">🔱 VMAX RADAR DE MILLONES 🔱</h1>
            <div style="border:2px solid #0f0; padding:20px; border-radius:10px; background:#111;">
                <h2 style="color:#fff;">ESTADO: BUSCANDO PRODUCTOS GANADORES...</h2>
                <p>Enfoque: Dropshipping & E-commerce Puro</p>
                <p>Margen objetivo: 70% - 85%</p>
            </div>
        </body>
    `);
});

app.listen(PORT, () => console.log('Radar VMAX activo'));
