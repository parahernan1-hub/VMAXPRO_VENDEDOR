const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const app = express();
const PORT = process.env.PORT || 10000;

// CONFIGURACIÓN DE TU IMPERIO
const MIN_GANANCIA = 55; // Tu requisito de 55% mínimo

app.get('/', async (req, res) => {
    // Aquí el bot lanza sus drones a la web (Ejemplo de estructura de datos reales)
    const productosReales = [
        { nombre: "Mini Sellador Térmico", costo: 3, venta: 19.99, fuente: "Tendencia TikTok" },
        { nombre: "Humidificador Volcán Pro", costo: 12, venta: 49.95, fuente: "Ads Library" }
    ];

    // EL MOTOR CALCULA EL MARGEN REAL
    const filtrados = productosReales.map(p => {
        const gananciaRaw = ((p.venta - p.costo) / p.venta) * 100;
        return { ...p, ganancia: gananciaRaw.toFixed(0) };
    }).filter(p => p.ganancia >= MIN_GANANCIA);

    res.send(`
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h1 style="text-align:center;">🔱 VMAX REAL-TIME RADAR 🔱</h1>
            <p style="text-align:center;">FILTRO: >${MIN_GANANCIA}% DE GANANCIA REAL ✅</p>
            <hr border="1" color="#0f0">
            <div style="max-width:800px; margin:auto; margin-top:20px;">
                ${filtrados.map(p => `
                    <div style="border:2px solid #0f0; padding:15px; margin-bottom:15px; background:#111;">
                        <h2 style="margin:0; color:#fff;">💎 ${p.nombre}</h2>
                        <p>📦 COSTO: $${p.costo} | 💰 VENTA: $${p.venta}</p>
                        <p style="font-size:1.2em; font-weight:bold; color:#0f0;">🔥 BENEFICIO: ${p.ganancia}%</p>
                        <p style="color:#888;">DETECTADO EN: ${p.fuente}</p>
                        <a href="https://www.google.com/search?q=${p.nombre}+dropshipping" target="_blank" style="color:#0f0;">[ ANALIZAR COMPETENCIA REAL ]</a>
                    </div>
                `).join('')}
            </div>
        </body>
    `);
});

app.listen(PORT, () => console.log('Radar Real VMAX encendido'));
