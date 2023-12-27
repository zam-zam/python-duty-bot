from datetime import datetime
from collections import deque
from typing import Deque, Dict, Union

from models.person import Person


class Duty:
    MAX_DUTY_HISTORY_LENGTH: int = 10

    def __init__(self, person: Person = None) -> None:
        self.__person = person
        self.__start_date = datetime.now()
        self.__update_date = datetime.now()
        self.__duty_history: Deque[Dict[str, Union[Person, datetime]]] = deque(maxlen=Duty.MAX_DUTY_HISTORY_LENGTH)

    @property
    def person(self) -> Person:
        return self.__person

    @person.setter
    def person(self, person: Person) -> None:
        self.__person = person
        self.__update_date = datetime.now()
        self.__duty_history.append({'person': person,
                                    'datetime': self.__update_date})

    @property
    def start_date(self, format: str = '%d.%m.%Y %H:%M') -> str:
        return self.__start_date.strftime(format)

    @property
    def update_date(self, format: str = '%d.%m.%Y %H:%M') -> str:
        return self.__update_date.strftime(format)

    @property
    def duty_history(self) -> Deque:
        return self.__duty_history