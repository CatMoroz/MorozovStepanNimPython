from random import choice, randint, shuffle

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


def make_bad_step(state_curr: list[int]) -> NimStateChange:
    heaps_list = list(range(len(state_curr)))
    shuffle(heaps_list)
    for heap in heaps_list:
        if state_curr[heap] != 0:
            return NimStateChange(heap, randint(1, state_curr[heap]))
    raise RuntimeError("It can be only if all heaps is empty")


def make_good_step(state_curr: list[int]) -> NimStateChange:
    bit_sum = 0
    for heap in state_curr:
        bit_sum ^= heap

    for heap in range(len(state_curr)):
        if (bit_sum ^ state_curr[heap]) < state_curr[heap]:
            return NimStateChange(heap, state_curr[heap] - (bit_sum ^ state_curr[heap]))
        else:
            return make_bad_step(state_curr)
    raise RuntimeError("It can be only if amount of heaps is 0")


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels  # уровень сложности

    def __init__(self, level: str) -> None:
        if isinstance(level, str) and level in [item.value for item in AgentLevels]:
            self._level = level
        else:
            raise ValueError("Bots' level can be only easy, normal or hard", level)

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        if self._level == AgentLevels.EASY:
            return make_bad_step(state_curr)
        elif self._level == AgentLevels.NORMAL:
            return choice([make_bad_step(state_curr), make_good_step(state_curr)])
        else:
            return make_good_step(state_curr)
