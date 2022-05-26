import requests
import datetime
from utils.holiday_date import get_uniq_holidays
from loguru import logger

from Settings.config import test_date


class Sender:
    def __init__(self, bitrix_webhook: str):
        logger.info('Starting...')
        self.bitrix_webhook: str = bitrix_webhook
        self.uniq_holidays: list = get_uniq_holidays()
        self.days_delta: datetime.timedelta = datetime.timedelta(days=3)
        self.bitrix_method: str = 'tasks.task.add'
        logger.add('logs/logs.log', format="{time} {level} {message}")

    def start_send_tasks(self):
        is_new_period: bool = True
        current_holiday_date: datetime.date = datetime.date(2000, 1, 1)
        logger.info('... done')
        while True:
            today: datetime.date = datetime.date.today()

            if test_date:
                today = datetime.datetime.strptime(test_date, '%Y-%m-%d').date()

            possible_holiday = today + self.days_delta

            if possible_holiday in self.uniq_holidays and is_new_period:
                current_holiday_date = possible_holiday
                body: dict = {
                    'fields':
                        {
                            'TITLE': 'pre-holiday task',
                            'CREATED_BY': 1,
                            'RESPONSIBLE_ID': 1,
                            'DEADLINE': current_holiday_date.strftime('%d-%m-%Y')
                        }
                }

                resp: requests.Response = requests.post(self.bitrix_webhook + self.bitrix_method, json=body)
                format_resp: dict = resp.json()

                if format_resp.get('error') is None:
                    logger.info(format_resp)
                else:
                    logger.error(format_resp)

                is_new_period = False

            if today == current_holiday_date + datetime.timedelta(days=1) and not is_new_period:
                is_new_period = True  # обновляем флаг только после праздника
                # может быть ситуация, когда между праздниками до 3х (таких вроде нет, но мб добавят) дней и в текущей
                # реализации задача не будет поставлена перед следующим праздником, но если это не обычное уведомление
                # о празднике, а задача, на которую дается 3 дня, то думаю лучше не сжимать сроки
