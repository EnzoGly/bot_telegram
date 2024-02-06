import telebot
from gerencianet import Gerencianet
import qrcode
import os
from datetime import datetime
import requests

# Configurações da API da Gerencianet
credentials = {
    'client_id': '#',
    'client_secret': '#',
    'certificate': 'C:\\Users\\enzob\\Downloads\\homologacao-546680-bot.p12',
    'sandbox': True  # Mude para False quando mover para produção
}

# Inicializa a GerenciaNet
gn = Gerencianet(credentials)

# Token da API do Telegram
API_TOKEN = '#'
bot = telebot.TeleBot(API_TOKEN)


# Função para lidar com o comando de compra
@bot.message_handler(commands=['comprar'])
def handle_buy(message):
    # Preço do produto ou serviço a ser cobrado via PIX
    valor_do_produto = '10.00'  # Valor a ser substituído pelo preço do produto
    # Sua chave PIX
    chave_pix = 'peguei99@gmail.com'  # Substitua pela sua própria chave PIX

    # Cria o corpo da cobrança PIX
    body = {
        'calendario': {
            'expiracao': 3600
        },
        'valor': {
            'original': valor_do_produto
        },
        'chave': chave_pix,
        'solicitacaoPagador': 'Descrição do pagamento'
    }

    # Cria uma cobrança PIX imediata
    response = gn.pix_create_immediate_charge(body=body)
    loc_id = response['loc']['id']

    # Gera a imagem do QR Code
    qrcode_image = get_qrcode_image(loc_id)
    with open(qrcode_image, 'rb') as qr_img:
        bot.send_photo(message.chat.id, qr_img)
        bot.send_message(message.chat.id,
                         'Por favor, escaneie o QR Code para pagar e envie /confirmar após realizar o pagamento.')


# Função para gerar a imagem do QR Code
def get_qrcode_image(loc_id):
    # Gera o QR Code através da GerenciaNet
    response = gn.pix_generate_qrcode(loc_id)
    imagem_qrcode = response['imagemQrcode']

    qr = qrcode.QRCode()
    qr.add_data(imagem_qrcode)
    qr.make()
    img_qr = qr.make_image(fill_color="black", back_color="white")
    # Salva a imagem do QR Code
    file_path = "qrcode_pago_pix.png"
    img_qr.save(file_path)
    return file_path


# Função para lidar com o comando de confirmação
@bot.message_handler(commands=['confirmar'])
def handle_confirmation(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Validando pagamento...')

    # Aqui você deve adicionar a lógica para verificar se o pagamento foi realizado
    # Isto pode envolver a chamada para a API da GerenciaNet ou a verificação de um webhook
    if check_payment_status(chat_id):
        enviar_video_aleatorio(chat_id)
    else:
        bot.send_message(chat_id, 'Pagamento ainda não foi confirmado.')


# Função para verificar o status do pagamento
def check_payment_status(chat_id):
    # Substitua pelo método de verificação do pagamento
    # Você precisará implementar a lógica de consulta à API da GerenciaNet ou verificar o webhook apropriado
    return True  # Deve se tornar dinâmico com base na resposta da API GerenciaNet


# Função para enviar um vídeo aleatório
def enviar_video_aleatorio(chat_id):
    # Aqui você deve adicionar a lógica para selecionar e enviar um vídeo aleatório
    # Este é um exemplo usando um caminho para um vídeo estático
    video_path = '"C:\\Users\\enzob\Videos\\video1.mkv"'  # Substitua pelo caminho real do vídeo
    with open(video_path, 'rb') as video:
        bot.send_video(chat_id, video)


# Começa a perguntar por novas mensagens
bot.polling(none_stop=True)