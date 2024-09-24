const express = require('express');
const { exec } = require('child_process');
const cron = require('node-cron');

const app = express();
const port = process.env.PORT || 8080;

// Caminho para o script Python
const pythonScript = './script.py';

// Função para executar o script Python
function runPythonScript() {
    exec(`python3 ${pythonScript}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Erro ao executar o script: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Erro no script: ${stderr}`);
            return;
        }
        console.log('Script executado!');
    });
}

// Agendar o script para rodar a cada 10 segundos
cron.schedule('*/10 * * * *', () => {
    console.log('Executando script Python a cada 10 minutos...');
    runPythonScript();
});

console.log('Agendador iniciado...');

// Configurar uma rota simples
app.get('/', (req, res) => {
    res.send('Web App está rodando e o script Python está sendo executado periodicamente a cada 10 segundos.');
});

// Iniciar o servidor
app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`);
});
