from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

with open('auth', 'r') as auth_file:
    api_id = int(auth_file.readline())
    api_hash = auth_file.readline()
    my_id = int(auth_file.readline())
client = TelegramClient('tagall', api_id, api_hash)


def start_bot():
    client.start()
    client.run_until_disconnected()


@client.on(events.ChatAction())
async def cmd_new_chat(event):
    if event.user.id == my_id:
        await cmd_start(event)


@client.on(events.NewMessage(pattern='/tagall', outgoing=False))
async def cmd_tagall(event: Message):
    reply_to = None
    chat = await event.get_chat()
    users = await client.get_participants(chat)
    requester = await event.get_sender()

    if event.is_reply:
        reply_to = event.reply_to.reply_to_msg_id
        msg_body = 'попросил всех обратить внимание на это сообщение'
    else:
        msg_body = 'призвал всех участников чата'

    result_msg = f'[{requester.first_name}](tg://user?id={requester.id}) ' \
                 f'{msg_body}' \
                 f'\n\n'
    result_msg += ''.join(
        map(lambda u: f'[.](tg://user?id={u.id})', users)
    )
    await client.send_message(chat, result_msg, reply_to=reply_to)


@client.on(events.NewMessage(pattern='/start', outgoing=False))
async def cmd_start(event):
    await event.reply(
        'Прив, я бот, тегающий всех участников чата\n'
        'Не спамящий в чат, быстрый и [опенсорсный](https://github.com/llistochek/open-tagall-bot)\n'
        'Чтобы начать меня использовать просто добавь меня в группу и напиши /tagall. '
        'Также, если ты хочешь чтобы все обратили внимание на сообщение, ответь на него командой /tagall\n\n'
        'Автор:\n'
        '[@llistochek](tg://user?id=889847837)'
    )


if __name__ == '__main__':
    start_bot()
