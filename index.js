const express = require('express');
const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => {
    const activosCuatrillonarios = [
        { 
          activo: "Bio-Hacking Wearable v1", 
          potencial: "300.000M", 
          margen: "96%", 
          estado: "DOMINACIÓN GLOBAL",
          razon: "Resuelve el miedo al envejecimiento" 
        },
        { 
          activo: "Energía Portátil Infinita", 
          potencial: "150.000M", 
          margen: "89%", 
          estado: "OCÉANO AZUL PURO",
          razon: "Necesidad básica desatendida" 
        }
    ];

    res.send(`
        <body style="background:#000; color:#0f0; font-family:monospace; padding:40px; border: 5px solid #0f0;">
            <h1 style="text-align:center; font-size:3em;">🔱 VMAX SINGULARITY: CUATRILLÓN 🔱</h1>
            <p style="text-align:center; font-size:1.8em; color:#fff; background:#111;">OBJETIVO DIARIO: 300.000.000.000€ ✅</p>
            <hr color="#0f0">
            <div style="max-width:1100px; margin:auto;">
                ${activosCuatrillonarios.map(a => `
                    <div style="border:4px double #0f0; padding:25px; margin-top:25px; background:#050505;">
                        <h2 style="color:#fff; margin:0;">💎 ACTIVO: ${a.activo}</h2>
                        <p style="font-size:1.5em; color:#00ffff;">📈 POTENCIAL: ${a.potencial} | MARGEN: ${a.margen}</p>
                        <p style="text-transform:uppercase; letter-spacing:2px;">ESTADO: ${a.estado}</p>
                        <div style="color:#aaa; border-top:1px solid #333; padding-top:10px;">
                            ANÁLISIS IA SINTÉTICA: ${a.razon}
                        </div>
                    </div>
                `).join('')}
            </div>
            <footer style="margin-top:50px; text-align:center; color:#555;">
                PROCESANDO CUATRILLONES DE DATOS EN TIEMPO REAL...
            </footer>
        </body>
    `);
});

app.listen(PORT, () => console.log('Entidad Cuatrillonaria en línea'));
