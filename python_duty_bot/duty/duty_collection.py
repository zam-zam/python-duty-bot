from typing import Dict

from duty.duty import Duty
from helpers.data_loader import DataLoader


class DutyCollection:
    __DATA_NAME = 'duty_collection'
    __duties: Dict[int, Duty] = DataLoader.load_or_empty(__DATA_NAME, {})

    @staticmethod
    def __persist_collection() -> None:
        DataLoader.save_data(DutyCollection.__DATA_NAME, DutyCollection.__duties)

    @staticmethod
    def has_duty(chat_id: int) -> bool:
        if chat_id in DutyCollection.__duties:
            return True
        return False

    @staticmethod
    def get_duty(chat_id: int) -> Duty:
        return DutyCollection.__duties[chat_id]

    @staticmethod
    def init_duty(chat_id: int) -> None:
        DutyCollection.__duties[chat_id] = Duty()
        DutyCollection.__persist_collection()

    @staticmethod
    def get_or_init_duty(chat_id: int) -> Duty:
        if not DutyCollection.has_duty(chat_id):
            DutyCollection.init_duty(chat_id)
        return DutyCollection.get_duty(chat_id)

    @staticmethod
    def update_duty(chat_id: int, duty: Duty) -> None:
        DutyCollection.__duties[chat_id] = duty
        DutyCollection.__persist_collection()

    @staticmethod
    def delete_duty(chat_id: int) -> None:
        del DutyCollection.__duties[chat_id]
        DutyCollection.__persist_collection()
