import pytest
import interfaces.googai_module as GoogAI
import config.configuration_module as Config

config = Config.Config()
ai_connect = GoogAI.GoogAI(api_key = config.google_ai_api_key)

def test_text_request():
    text_content = "Напиши только слово 'проверка' и ничего больше."
    assert ai_connect.text_request(text_content = text_content) == "проверка"