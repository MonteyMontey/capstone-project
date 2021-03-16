class EnvInterface:

    def reset(self) -> object:
        pass

    def step(self, action) -> tuple:
        pass

    def screenshot(self) -> object:
        pass
