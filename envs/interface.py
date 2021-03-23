from .action import Action


class EnvInterface:

    def reset(self) -> object:
        pass

    def step(self, action: Action) -> tuple:
        pass

    def screenshot(self) -> object:
        pass

    def get_state(self) -> object:
        pass
