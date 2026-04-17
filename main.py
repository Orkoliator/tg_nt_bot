import interfaces.tg_module as TelegramInterface
import config.configuration_module as Config
import interfaces.sql_module as SqlConnect

from async_cron.job import CronJob
from async_cron.schedule import Scheduler

import asyncio

config = Config.Config()

scheduler = Scheduler(locale="pl-PL")

def main():
    SqlConnect.SqlConnect().create_tables()
    loop = asyncio.get_event_loop()
    #scheduler.add_job(some_job_by_time)
    TelegramInterface.TelegramConnect(config.telegram_api_id, config.telegram_api_hash, config.telegram_bot_token).run()
    #try:
    #    loop.run_until_complete(scheduler.start())
    #except KeyboardInterrupt:
    #    print('[ERROR] exited manually')

if __name__ == "__main__":
    main()