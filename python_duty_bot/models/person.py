class Person:
    def __init__(self, telegram_id: int, name: str):
        self.telegram_id = telegram_id
        self.name = name.lstrip('@')

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def telegram_id(self) -> int:
        return self._telegram_id

    @telegram_id.setter
    def telegram_id(self, telegram_id: int) -> None:
        self._telegram_id = telegram_id
