from telethon import TelegramClient, events, Button

# Configurações da API do Telegram (substitua com suas credenciais)
api_id = '17722891'
api_hash = '9afd06e5c607be33304e94fffb26ecb5'
bot_token = '7352140241:AAHdZdOPjCCWF98KXyExQ8UZSPpcTW4Y65s'

# Inicializando o bot
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Variável global para armazenar o arquivo atual (imagem ou vídeo)
current_media = None

# Função para enviar a mensagem com a mídia (imagem ou vídeo) e botões
async def send_message_with_buttons(event, media=None):
    global current_media
    # Se uma nova mídia for fornecida, atualize o arquivo atual
    if media:
        current_media = media
    
    # Enviar o arquivo de mídia atual com a mensagem e botões
    await client.send_file(event.chat_id, file=current_media, caption="🔞 Bem-vindo(a)! Aqui, o prazer é apenas para quem sabe apreciar. Cada conteúdo foi cuidadosamente selecionado para despertar seus desejos mais intensos. Quer sentir um gostinho? 😈 O próximo passo pode te levar a algo que você nunca experimentou antes!",
                           buttons=[
                               [Button.url("🔞 Entrar no Grupo de Prévias", "https://t.me/+16f2Xu3XwyBmMmQx")],
                               [Button.inline("Sair do Grupo", b"exit")]
                           ])

# Comando para enviar a mensagem com mídia
@client.on(events.NewMessage(pattern='/enviar'))
async def handler(event):
    await send_message_with_buttons(event)

# Comando para atualizar a mídia (imagem ou vídeo) e enviar a nova mensagem
@client.on(events.NewMessage(pattern='/atualizar_midia'))
async def update_media(event):
    if event.message.media:  # Verifica se um arquivo de mídia (imagem ou vídeo) foi enviado
        media = await event.download_media()
        await send_message_with_buttons(event, media=media)
        await event.reply("Mídia atualizada com sucesso!")
    else:
        await event.reply("Envie uma imagem ou vídeo junto com o comando!")

# Limpeza de mensagens de entradas e saídas, incluindo "sair e denunciar"
@client.on(events.ChatAction)
async def handle_new_member(event):
    # Remover mensagens de entrada, saída e remoção de membros
    if event.user_added or event.user_joined or event.user_left or event.user_kicked:
        await event.delete()

# Ação para remover um membro sem banimento e apagar a mensagem de remoção
@client.on(events.CallbackQuery(data=b'exit'))
async def remove_member(event):
    user = await event.get_sender()
    # Remover o participante sem banir
    await client.kick_participant(event.chat_id, user.id)  
    await event.delete()  # Apaga a mensagem de remoção
    # Tenta apagar qualquer mensagem de serviço sobre a remoção
    async for message in client.iter_messages(event.chat_id):
        if message.sender_id == user.id and message.action_message:
            await message.delete()

    await event.answer("Você foi removido do grupo, mas pode voltar pelo link de convite!")

# Rodar o bot
print("Bot rodando...")
client.run_until_disconnected()
