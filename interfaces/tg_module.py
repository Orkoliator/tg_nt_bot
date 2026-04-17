from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat

from logic.telegram_logic import TelegramLogic


class TelegramConnect:

    def __init__(self, api_id, api_hash, bot_token):
        self.client = TelegramClient(
            "handle_session",
            api_id,
            api_hash
        ).start(bot_token=bot_token)

        self.register_handlers()

    def register_handlers(self):

        @self.client.on(events.NewMessage(pattern=r"^/\w+$"))
        async def command_handler(event):
            if not isinstance(event.message.peer_id, (PeerUser, PeerChat)):
                return

            self.logic = TelegramLogic()

            chat_id_int = await self.client.get_entity(event.message.peer_id)
            chat_id_int = chat_id_int.id
            text = self.logic.message_route(event.raw_text.strip(), chat_id_int)

            await self.client.send_message(event.message.peer_id, text)

    def run(self):
        self.client.run_until_disconnected()