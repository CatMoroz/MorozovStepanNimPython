from random import randint

from nim_game.common.models import NimStateChange

STONES_AMOUNT_MIN = 1  # минимальное начальное число камней в кучке
STONES_AMOUNT_MAX = 10  # максимальное начальное число камней в кучке
HEAPS_AMOUNT_MIN = 2  # минимальное начальное число кучек в кучке
HEAPS_AMOUNT_MAX = 10  # максимальное начальное число кучек в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]  # кучки

    def __init__(self, heaps_amount: int) -> None:
        if isinstance(heaps_amount, int):
            if HEAPS_AMOUNT_MIN <= heaps_amount <= HEAPS_AMOUNT_MAX:
                self._heaps = [randint(STONES_AMOUNT_MIN, STONES_AMOUNT_MAX)
                               for _ in range(heaps_amount)
                               ]
            else:
                raise ValueError("Amount of heaps must be in range [2, 10]")
        else:
            raise ValueError("Amount of heaps must be integer")

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек

        :return: копия списка с кучек
        """
        return self._heaps

    def change_state(self, state_change: NimStateChange) -> None:
        """
        Изменения текущего состояния кучек

        :param state_change: структура описывающая изменение состояния
        """
        if state_change.heap_id < 0 or state_change.heap_id >= len(self._heaps):
            raise ValueError("Heap id doesn't in range")
        if state_change.decrease < 1 or state_change.decrease > self._heaps[state_change.heap_id]:
            raise ValueError("Bad amount taken stones")
        self._heaps[state_change.heap_id] -= state_change.decrease

    @property
    def heaps(self) -> list[int]:
        return self._heaps
