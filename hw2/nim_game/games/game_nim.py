import json

from nim_game.common.enumerations import Players
from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent


class GameNim:
    _environment: EnvironmentNim  # состояния кучек
    _agent: Agent  # бот

    def __init__(self, path_to_config: str) -> None:
        with open(path_to_config, 'r', encoding='utf-8') as f:
            text = json.load(f)
            heaps_amount = int(text["heaps_amount"])
            opponent_level = str(text["opponent_level"])

            self._environment = EnvironmentNim(heaps_amount)
            self._agent = Agent(opponent_level)

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """
        player_step.heap_id -= 1
        self._environment.change_state(player_step)
        if self.is_game_finished():
            return GameState(Players.USER)
        opponent_step = self._agent.make_step(self._environment.heaps)
        self._environment.change_state(opponent_step)
        if self.is_game_finished():
            return GameState(Players.BOT)
        return GameState(None, opponent_step, self._environment.heaps)

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        if any(self._environment.heaps):
            return False
        else:
            return True

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
