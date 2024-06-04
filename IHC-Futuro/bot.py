import logging
import re
from telegram import Update, InputMediaPhoto
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
    def __init__(self, modelo, preco, tamanho, foto_url):
        self.modelo = modelo
        self.preco = preco
        self.tamanho = tamanho
        self.foto_url = foto_url

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

# Lista de tênis disponíveis na loja com URLs de fotos
tenis_disponiveis = [
    Tenis("Nike Air Max", 299.99, "36-45", "https://imgnike-a.akamaihd.net/1300x1300/010228IE.jpg"),
    Tenis("Adidas Ultraboost", 259.99, "37-44", "https://assets.adidas.com/images/w_600,f_auto,q_auto/fc885d1de97246fc9183af9000da38a8_9366/Tenis_Ultraboost_Light_23_Preto_HQ6340_01_standard.jpg"),
    Tenis("Puma RS-X", 199.99, "38-42", "https://ostoresneakers.vteximg.com.br/arquivos/ids/220455-1000-1000/tenis-puma-rs-x-suede-v-branco-verde-396361-06-0.jpg?v=638321167759730000"),
    Tenis("Asics Gel-Kayano", 379.99, "36-44", "https://www.utennis.com.br/media/catalog/product/cache/89bf88682659cca671013fd904f60135/1/0/1011a767.021-tenis-asics-gel-kayano-27-masculino-cinza-e-azul-petroleo.jpeg"),
    Tenis("Mizuno Wave Prophecy", 499.99, "38-45", "https://mizunobr.vtexassets.com/arquivos/ids/234718-800-800?v=638247614107070000&width=800&height=800&aspect=true"),
    Tenis("New Balance 1080v11", 299.99, "37-43", "https://imgcentauro-a.akamaihd.net/1366x1366/96046604.jpg"),
    Tenis("Reebok Zig Kinetica", 289.99, "35-44", "https://img.joomcdn.net/86fde1725777127ef4c01f94b6f1ce4ff75ff505_1024_1024.jpeg"),
    Tenis("Fila Disruptor", 189.99, "36-41", "https://fila.vtexassets.com/arquivos/ids/898750/5XM01765_125.jpg?v=638254809484470000"),
    Tenis("Under Armour HOVR Phantom", 399.99, "38-44", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbuNnHLmHn_8w2piEyynX7-TvtsrKqKj4Uig&s"),
    Tenis("Saucony Triumph 18", 349.99, "37-44", "https://static.netshoes.com.br/produtos/tenis-saucony-triumph-18-i-feminino/22/311-3231-022/311-3231-022_zoom5.jpg?ts=1692070491&ims=544x")
]

# Função para lidar com o comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Eu sou o bot da loja de tênis. Como posso ajudar?')
    context.user_data.clear()

# Função para lidar com as mensagens de texto
def reply_to_message(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    response = generate_response(message, update, context)
    update.message.reply_text(response)

# Função para processar a mensagem e gerar uma resposta
def generate_response(message: str, update: Update, context: CallbackContext) -> str:
    doc = nlp(message)
    text = message.lower()

    # Verificar se estamos no meio de uma compra
    if context.user_data.get("comprando"):
        if re.search(r'\bcancelar\b|\bmudei de ideia\b|\bquero cancelar\b', text):
            return desistir_compra(context)
        else:
            return processar_compra(text, context)

    # Verificar palavras-chave relevantes e contexto de modelo
    if re.search(r'\bmodelo[s]?\b', text):
        return get_modelos_disponiveis()
    elif re.search(r'\btamanho[s]?\b', text):
        return get_tamanhos_disponiveis(context)
    elif re.search(r'\bbarato\b|\bmais barato\b', text):
        return get_tenis_mais_barato()
    elif re.search(r'\bpreço\b|\bpreços\b', text):
        return get_precos()
    elif re.search(r'\bcomprar\b|\bcompra\b', text):
        return iniciar_compra(text, context)
    elif re.search(r'\bpagamento\b|\bformas de pagamento\b', text):
        return get_formas_pagamento()
    elif re.search(r'\bfoto[s]?\b|\bimagem\b|\bfotos\b|\bimagens\b', text):
        return enviar_fotos_tenis(update, context)
    else:
        for tenis in tenis_disponiveis:
            if re.search(r'\b' + re.escape(tenis.modelo.lower().split()[0]) + r'\b', text):
                context.user_data["modelo"] = tenis.modelo
                return get_info_tenis(tenis.modelo)

        if "modelo" in context.user_data:
            return get_info_tenis(context.user_data["modelo"])

        return 'Desculpe, não entendi. Posso te ajudar com informações sobre modelos, tamanhos e preços de tênis ou com a compra de um modelo específico.'

# Funções específicas para gerar respostas
def get_modelos_disponiveis() -> str:
    modelos = "\n".join([f"- {tenis.modelo}" for tenis in tenis_disponiveis])
    return f'Os modelos disponíveis são:\n{modelos}'

def get_tamanhos_disponiveis(context: CallbackContext) -> str:
    if "modelo" in context.user_data:
        modelo = context.user_data["modelo"]
        for tenis in tenis_disponiveis:
            if tenis.modelo == modelo:
                tamanhos = ", ".join(map(str, tenis.tamanhos_disponiveis()))
                return f'Os tamanhos disponíveis para o {modelo} são: {tamanhos}'
    return 'Por favor, mencione um modelo específico para ver os tamanhos disponíveis.'

def get_tenis_mais_barato() -> str:
    tenis_barato = min(tenis_disponiveis, key=lambda tenis: tenis.preco)
    return f'O tênis mais barato é o {tenis_barato.modelo} por R${tenis_barato.preco:.2f}'

def get_precos() -> str:
    precos = "\n".join([f'{tenis.modelo}: R${tenis.preco:.2f}' for tenis in tenis_disponiveis])
    return f'Os preços dos tênis são:\n{precos}'

def get_info_tenis(modelo: str) -> str:
    for tenis in tenis_disponiveis:
        if tenis.modelo.lower() == modelo.lower():
            tamanhos = ", ".join(map(str, tenis.tamanhos_disponiveis()))
            return (f'O {tenis.modelo} está disponível nos tamanhos {tamanhos} '
                    f'por R${tenis.preco:.2f}.')
    return 'Modelo não encontrado.'

def iniciar_compra(text: str, context: CallbackContext) -> str:
    if "modelo" in context.user_data:
        modelo = context.user_data["modelo"]
        for tenis in tenis_disponiveis:
            if tenis.modelo == modelo:
                context.user_data["comprando"] = True
                tamanhos = ", ".join(map(str, tenis.tamanhos_disponiveis()))
                return (f'Perfeito! Você deseja comprar o {tenis.modelo}. '
                        f'Ele custa R${tenis.preco:.2f} e está disponível nos tamanhos {tamanhos}. '
                        'Qual tamanho você gostaria de comprar?')
    return 'Por favor, diga o modelo do tênis que você deseja comprar.'

def processar_compra(text: str, context: CallbackContext) -> str:
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
        tamanho = context.user_data["tamanho"]
        context.user_data.clear()  # Limpa o estado de contexto após a compra
        return (f'Obrigado pela sua compra! Você escolheu o {modelo} no tamanho {tamanho}. '
                'Sua compra foi realizada com sucesso!')

def get_formas_pagamento() -> str:
    return 'Aceitamos as seguintes formas de pagamento:\n- Cartão de crédito\n- Débito\n- Boleto bancário\n- Pix'

def enviar_fotos_tenis(update: Update, context: CallbackContext) -> str:
    if "modelo" in context.user_data:
        modelo = context.user_data["modelo"]
        for tenis in tenis_disponiveis:
            if tenis.modelo.lower() == modelo.lower():
                update.message.reply_photo(tenis.foto_url, caption=f'Foto do {tenis.modelo}')
                return 'Aqui está a foto do modelo que você pediu.'
    return 'Por favor, mencione o modelo do tênis que você gostaria de ver a foto.'

def desistir_compra(context: CallbackContext) -> str:
    if context.user_data.get("comprando"):
        context.user_data.clear()
        return 'A compra foi cancelada com sucesso. Como mais posso te ajudar?'
    else:
        return 'Você não está no meio de uma compra.'

# Função principal
def main() -> None:
    updater = Updater("7183875421:AAETZbIULAPkG0FYM4mlRpnE8c50Qbz82zc", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


#"7183875421:AAETZbIULAPkG0FYM4mlRpnE8c50Qbz82zc