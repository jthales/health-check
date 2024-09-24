import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017/')  # URL de conexão ao MongoDB
db = client['nome_do_banco']  # Nome do banco de dados
collection = db['nome_da_colecao']  # Nome da coleção onde as APIs estão armazenadas

# URL do webhook do Discord
discord_webhook_url = 'https://discord.com/api/webhooks/1278738599646597273/-ATZcKQUNR7-3CJENKwaf0lLZhm10dNCVBN1TQDSDwd7HNIVTjA2rGyn6eY1sM0YgwtL'

# Função para buscar APIs no MongoDB
def get_apis_from_db():
    return list(collection.find({}, {'_id': 0, 'alias': 1, 'url': 1, 'corpo': 1, 'metodo': 1, 'cabecalho': 1}))

# Função para verificar o status de uma API
def check_api_status(api):
    try:
        headers = {header['propriedade']: header['valor'] for header in api.get('cabecalho', [])}
        if api['metodo'].upper() == 'POST':
            response = requests.post(api['url'], json=api.get('corpo', {}), headers=headers, timeout=10)
        else:
            response = requests.get(api['url'], headers=headers, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False

# Função para enviar notificação no Discord
def send_discord_notification(api):
    webhook = DiscordWebhook(url=discord_webhook_url)
    embed = DiscordEmbed(title=f'{api["alias"]} Offline', description=f'A API em {api["url"]} está fora do ar!', color='FF0000')
    webhook.add_embed(embed)
    webhook.execute()

# Função para monitorar as APIs
def monitor_apis():
    apis = get_apis_from_db()
    
    for api in apis:
        if not check_api_status(api):
            send_discord_notification(api)

# Execução do script
if __name__ == '__main__':
    monitor_apis()
