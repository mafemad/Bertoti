import logging
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import spacy

# Configuração do logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Certifique-se de que o modelo de linguagem do spaCy está instalado
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    logging.error("Modelo pt_core_news_sm não encontrado. Por favor, instale o modelo usando 'python -m spacy download pt_core_news_sm'")
    raise

# Classe para representar um produto da loja de tênis
class Tenis:
    def __init__(self, modelo, preco, tamanho):
        self.modelo = modelo
        self.preco = preco
        self.tamanho = tamanho

    def tamanhos_disponiveis(self):
        # Retorna uma lista de tamanhos disponíveis
        tamanhos = []
        for tamanho in self.tamanho.split(','):
            if '-' in tamanho:
                start, end = map(int, tamanho.split('-'))
                tamanhos.extend(range(start, end + 1))
            else:
                tamanhos.append(int(tamanho))
        return tamanhos

# Lista de tênis disponíveis na loja
tenis_disponiveis = [
    Tenis("Nike Air Max", 299.99, "36-45"),
    Tenis("Adidas Ultraboost", 259.99, "37-44"),
    Tenis("Puma RS-X", 199.99, "38-42"),
    Tenis("Asics Gel-Kayano", 379.99, "36-44"),
    Tenis("Mizuno Wave Prophecy", 499.99, "38-45"),
    Tenis("New Balance 1080v11", 299.99, "37-43"),
    Tenis("Reebok Zig Kinetica", 289.99, "35-44"),
    Tenis("Fila Disruptor", 189.99, "36-41"),
    Tenis("Under Armour HOVR Phantom", 399.99, "38-44"),
    Tenis("Saucony Triumph 18", 349.99, "37-44")
]

# Função para lidar com o comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Eu sou o bot da loja de tênis. Como posso ajudar?')
    # Limpa o estado de contexto para uma nova sessão
    context.user_data.clear()

# Função para lidar com as mensagens de texto
def reply_to_message(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    response = generate_response(message, context)
    update.message.reply_text(response)

# Função para processar a mensagem e gerar uma resposta
def generate_response(message: str, context: CallbackContext) -> str:
    # Processar a mensagem usando o modelo do spaCy
    doc = nlp(message)
    text = message.lower()
    
    # Verificar se estamos no meio de uma compra
    if context.user_data.get("comprando"):
        return processar_compra(text, context)
    
    # Verificar palavras-chave relevantes
    if re.search(r'\bmodelo[s]?\b', text):
        return get_modelos_disponiveis()
    elif re.search(r'\btamanho[s]?\b', text):
        return get_tamanhos_disponiveis()
    elif re.search(r'\bbarato\b|\bmais barato\b', text):
        return get_tenis_mais_barato()
    elif re.search(r'\bpreço\b|\bpreços\b', text):
        return get_precos()
    elif re.search(r'\bcomprar\b|\bcompra\b', text):
        return iniciar_compra(text, context)
    elif re.search(r'\bpagamento\b|\bformas de pagamento\b', text):
        return get_formas_pagamento()
    else:
        for tenis in tenis_disponiveis:
            if re.search(tenis.modelo.lower(), text):
                return get_info_tenis(tenis.modelo)
        return 'Desculpe, não entendi. Posso te ajudar com informações sobre modelos, tamanhos e preços de tênis ou com a compra de um modelo específico.'

# Funções específicas para gerar respostas
def get_modelos_disponiveis() -> str:
    # Lista todos os modelos de tênis disponíveis na loja
    modelos = "\n".join([f"- {tenis.modelo}" for tenis in tenis_disponiveis])
    return f'Os modelos disponíveis são:\n{modelos}'

def get_tamanhos_disponiveis() -> str:
    # Lista todos os tamanhos disponíveis para os tênis
    tamanhos = sorted(set(tamanho for tenis in tenis_disponiveis for tamanho in tenis.tamanhos_disponiveis()))
    tamanhos_str = ", ".join(map(str, tamanhos))
    return f'Os tamanhos disponíveis são: {tamanhos_str}'

def get_tenis_mais_barato() -> str:
    # Informa qual é o tênis mais barato disponível
    tenis_barato = min(tenis_disponiveis, key=lambda tenis: tenis.preco)
    return f'O tênis mais barato é o {tenis_barato.modelo} por R${tenis_barato.preco:.2f}'

def get_precos() -> str:
    # Lista os preços de todos os tênis disponíveis
    precos = "\n".join([f'{tenis.modelo}: R${tenis.preco:.2f}' for tenis in tenis_disponiveis])
    return f'Os preços dos tênis são:\n{precos}'

def get_info_tenis(modelo: str) -> str:
    # Fornece informações detalhadas sobre um modelo específico de tênis
    for tenis in tenis_disponiveis:
        if tenis.modelo.lower() == modelo.lower():
            tamanhos = ", ".join(map(str, tenis.tamanhos_disponiveis()))
            return (f'O {tenis.modelo} está disponível nos tamanhos {tamanhos} '
                    f'por R${tenis.preco:.2f}.')
    return 'Modelo não encontrado.'

def iniciar_compra(text: str, context: CallbackContext) -> str:
    # Inicia o processo de compra para um modelo específico de tênis
    for tenis in tenis_disponiveis:
        if re.search(tenis.modelo.lower(), text):
            context.user_data["comprando"] = True
            context.user_data["modelo"] = tenis.modelo
            tamanhos = ", ".join(map(str, tenis.tamanhos_disponiveis()))
            return (f'Você escolheu comprar o {tenis.modelo}. '
                    f'Ele custa R${tenis.preco:.2f} e está disponível nos tamanhos {tamanhos}. '
                    'Qual tamanho você gostaria de comprar?')
    return 'Por favor, diga o modelo do tênis que você deseja comprar.'

def processar_compra(text: str, context: CallbackContext) -> str:
    # Processa o tamanho do tênis escolhido e pergunta a forma de pagamento
    modelo = context.user_data["modelo"]
    if not context.user_data.get("tamanho"):
        for tenis in tenis_disponiveis:
            if tenis.modelo == modelo:
                if text.isdigit() and int(text) in tenis.tamanhos_disponiveis():
                    context.user_data["tamanho"] = text
                    return ('Qual a forma de pagamento que você gostaria de usar?\n'
                            '- Cartão de crédito\n- Débito\n- Boleto bancário\n- Pix')
                else:
                    tamanhos = ", ".join(map(str, tenis.tamanhos_disponiveis()))
                    return f'Desculpe, o tamanho {text} não está disponível para o {tenis.modelo}. Por favor, escolha um tamanho entre {tamanhos}.'
    else:
        if text.lower() in ['cartão de crédito', 'débito', 'boleto bancário', 'pix']:
            forma_pagamento = text
            tamanho = context.user_data["tamanho"]
            context.user_data.clear()  # Limpa o estado de contexto após a compra
            return (f'Obrigado pela sua compra! Você escolheu o {modelo} no tamanho {tamanho} '
                    f'com pagamento via {forma_pagamento}. '
                    'Sua compra foi realizada com sucesso!')
        else:
            return ('Forma de pagamento inválida. Por favor, escolha uma das seguintes formas de pagamento:\n'
                    '- Cartão de crédito\n- Débito\n- Boleto bancário\n- Pix')

def get_formas_pagamento() -> str:
    # Informa as formas de pagamento aceitas pela loja
    return 'Aceitamos as seguintes formas de pagamento:\n- Cartão de crédito\n- Débito\n- Boleto bancário\n- Pix'

def main() -> None:
    # Criar um updater para receber as atualizações do Telegram
    #"7183875421:AAETZbIULAPkG0FYM4mlRpnE8c50Qbz82zc
    updater = Updater("TOKEN", use_context=True)

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
