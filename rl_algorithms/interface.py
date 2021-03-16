class AlgInterface:

    def choose_action(self, observation: list) -> object:
        pass

    def remember(self, state: list, action: object, reward: float, state_: list, done: bool) -> None:
        pass

    def learn(self) -> None:
        pass
