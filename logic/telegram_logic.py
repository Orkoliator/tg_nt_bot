import config.configuration_module as Config
import interfaces.sql_module as SqlConnect

class TelegramLogic:

    def __init__(self):
        self.emoji_dict = {
            "emoji_smiling_face_with_smiling_eyes": u'\U0001F60A',
            "emoji_smiling_face_with_open_mouth_and_cold_sweat": u'\U0001F605',
            "emoji_winking_face": u'\U0001F609'
        }
        config = Config.Config()
        self.sql_connect = SqlConnect.SqlConnect(db_file = config.db_file)

    def message_start_logic(self, peer_id):
        self.sql_connect.add_subscriber(chat_id_int = peer_id)
        return (
            f"Привет друг, меня зовут ПП Цыпа {self.emoji_dict["emoji_smiling_face_with_smiling_eyes"]}"
            f"Моя цель - помочь в организации твоего ЗОЖ "
            f"и для этого я могу предлагать тебе советы по "
            f"питанию и тренеровкам.\n"
            f"Пожалуйста напиши /help чтобы увидеть что я могу!"
        )

    def message_help_logic(self, peer_id):
        return (
            f"Вот список того что я умею:\n"
            f"/help - узнать что такое рекурсия.\n"
            f"/sub_workout - подписаться на рассылку тренировок\n"
            f"/sub_meals - подписаться на рассылку рецептов\n"
            f"/unsub_workout - отписаться от рассылки тренировок"
            f"/unsub_meals - отписаться от рассылки рецептов\n"
            f"Пожалуйста напечатай нужную команду или просто "
            f"нажми на нее в моем сообщении чтобы воспользоваться "
            f"ей {self.emoji_dict["emoji_smiling_face_with_smiling_eyes"]}"
        )

    def message_sub_workout(self, peer_id):
        self.sql_connect.update_subscribtion_type(chat_id_int = peer_id, subscription_type = "Workout", subscription_status = 1)
        return (
            f"Теперь ты подписан на рассылку плана тренировок!\n"
            f"Тренировки рассылкаются по следующему графику:\n"
            f"- вторник 16:15 CET\n"
            f"- четверг 16:15 CET\n"
            f"- суббота 16:15 CET\n"
            f"Тренировки строятся по принципу Full Body "
            f"с разным акцентом между тренировками и рассчитаны "
            f"на 60-90 минут."
            f"Чтобы отписаться используй команду "
            f"/unsub_workout"
        )

    def message_sub_meals(self, peer_id):
        self.sql_connect.update_subscribtion_type(chat_id_int = peer_id, subscription_type = "Recipes", subscription_status = 1)
        return (
            f"Теперь ты подписан на рассылку рецептов!\n"
            f"Рецепты рассылкаются каждый день по следующему "
            f"графику:\n"
            f"- завтрак - 8:00 CET\n"
            f"- обед  - 12:00 CET\n"
            f"- перекус -  16:00 CET\n"
            f"- список покупок на завтра -  16:10 CET\n"
            f"- ужин -  20:00 CET\n"
            f"Рецепты рассчитаны на 1500 ккал с учетом "
            f"балланса БЖУ."
            f"Чтобы отписаться используй команду "
            f"/unsub_meals"
        )

    def message_unsub_workout(self, peer_id):
        self.sql_connect.update_subscribtion_type(chat_id_int = peer_id, subscription_type = "Workout", subscription_status = 0)
        return (
            f"Рассылка плана тренировок приостановлена,\n"
            f"Приятного отдыха!{self.emoji_dict["emoji_smiling_face_with_open_mouth_and_cold_sweat"]}\n"
            f"Если захочешь возобновить рассылку - "
            f"используй команду /sub_workout {self.emoji_dict["emoji_winking_face"]}\n"
        )

    def message_unsub_meals(self, peer_id):
        self.sql_connect.update_subscribtion_type(chat_id_int = peer_id, subscription_type = "Recipes", subscription_status = 0)
        return (
            f"Рассылка рецептов приостановлена,\n"
            f"Приятного отдыха!{self.emoji_dict["emoji_smiling_face_with_open_mouth_and_cold_sweat"]}\n"
            f"Если захочешь возобновить рассылку - "
            f"используй команду /sub_meals {self.emoji_dict["emoji_winking_face"]}\n"
        )