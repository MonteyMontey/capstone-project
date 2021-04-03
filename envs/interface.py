from .action import Action


class EnvInterface:
    """The interface defines the methods which each environment class needs to implement"""

    def reset(self) -> object:
        """Resets the environment"""
        pass

    def step(self, action: Action) -> tuple:
        """Executes an action in the environment"""
        pass

    def screenshot(self) -> object:
        """Returns a screenshot of the environment"""
        pass

    def get_state(self) -> object:
        """Returns the state of the environment"""
        pass
