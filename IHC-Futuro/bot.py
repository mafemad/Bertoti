import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import spacy

# Configuração do logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar modelo do spaCy para processamento de linguagem natural em português
nlp = spacy.load("pt_core_news_sm")

# Classe para representar um produto da loja de tênis
class Tenis:
    def __init__(self, modelo, preco, tamanho):
        self.modelo = modelo
        self.preco = preco
        self.tamanho = tamanho

# Lista de tênis disponíveis na loja
tenis_disponiveis = [
    Tenis("Nike Air Max", 299.99, "36-45"),
    Tenis("Adidas Ultraboost", 259.99, "37-44"),
    Tenis("Puma RS-X", 199.99, "38-42")
]

# Função para lidar com o comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Eu sou o bot da loja de tênis. Como posso ajudar?')

# Função para lidar com as mensagens de texto
def reply_to_message(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    response = generate_response(message)
    update.message.reply_text(response)

# Função para processar a mensagem e gerar uma resposta
def generate_response(message: str) -> str:
    # Processar a mensagem usando o modelo do spaCy
    doc = nlp(message)
    
    # Verificar se a mensagem contém palavras-chave relevantes
    if any(token.text.lower() in ['modelo', 'modelos'] for token in doc):
        modelos = ", ".join([tenis.modelo for tenis in tenis_disponiveis])
        return f'Os modelos disponíveis são: {modelos}'
    elif any(token.text.lower() in ['tamanho', 'tamanhos'] for token in doc):
        tamanhos = ", ".join(set([tenis.tamanho for tenis in tenis_disponiveis]))
        return f'Os tamanhos disponíveis são: {tamanhos}'
    elif any(token.text.lower() in ['barato', 'mais barato'] for token in doc):
        tenis_barato = min(tenis_disponiveis, key=lambda tenis: tenis.preco)
        return f'O tênis mais barato é o {tenis_barato.modelo} por R${tenis_barato.preco:.2f}'
    else:
        return 'Desculpe, não entendi. Como posso ajudar?'

def main() -> None:
    # Criar um updater para receber as atualizações do Telegram
    updater = Updater("7183875421:AAETZbIULAPkG0FYM4mlRpnE8c50Qbz82zc", use_context=True)

    # Obter o despachante para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Registrar manipuladores para comandos e mensagens de texto
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_message))

    # Iniciar o bot
    updater.start_polling()

    # Executar o bot até que Ctrl+C seja pressionado
    updater.idle()

if __name__ == '__main__':
    main()






#pip install python-telegram-bot==13.7
#pip install spacy==3.0.6
