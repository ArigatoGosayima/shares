import cryptocompare
from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = 1277086  # your API ID
api_hash = '10257d27ba3d4b8f5eb80b29f3d4e98a'  # Your API Hash
phone = '+353863552124'  # your phone number
client = TelegramClient(phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        groups.append(chat)
    except:
        continue
print(groups)
print('Choose a group to set Trace on:')
i = 0
for g in groups:
    print(str(i) + ' - ' + g.title)
    i += 1
g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]
print('Choose a group to give to:')
i = 0
for g in groups:
    print(str(i) + ' - ' + g.title)
    i += 1
g_index = input("Enter a Number: ")
home_group = groups[int(g_index)]
print('Setting trace on: ' + str(target_group.title))
print('Setting destination as: ' + str(home_group.title))
message = ''
while True:
    @client.on(events.NewMessage(chats=target_group.id))
    async def my_event_handler(event):
        await client.forward_messages(home_group, event.message)
    client.start()
    client.run_until_disconnected()