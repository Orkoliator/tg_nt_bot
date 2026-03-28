from telethon import TelegramClient, events
from telethon.tl.types import PeerUser

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

        pattern_dict = {
            "/start": TelegramLogic.message_start_logic,
            "/help": TelegramLogic.message_help_logic,
            "/sub_workout": TelegramLogic.message_sub_workout,
            "/sub_meals": TelegramLogic.message_sub_meals,
            "/unsub_workout": TelegramLogic.message_unsub_workout,
            "/unsub_meals": TelegramLogic.message_unsub_meals,
        }

        @self.client.on(events.NewMessage(pattern=r"^/\w+$"))
        async def command_handler(event):
            if not isinstance(event.message.peer_id, PeerUser):
                return

            command = event.raw_text.strip()

            if command in pattern_dict:
                text = pattern_dict[command](event.message.peer_id)
                await event.respond(text)

    def run(self):
        self.client.run_until_disconnected()