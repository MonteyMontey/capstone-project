from .action import Action


class EnvInterface:
    """The interface defines the methods which each environment class needs to implement"""

    def reset(self) -> object:
        """Resets the environment

        Returns
            state (list[float]): The state of the environment"""
        pass

    def step(self, action: Action) -> tuple:
        """Executes an action in the environment

        Returns:
            state (list[float]): The new state of the environment after the action was executed.
            reward (float): The reward for the executed action.
            done (bool): done = True if snake dies, else done = False.
            score (int): How many pieces of food the snake ate so far.
        """
        pass

    def screenshot(self) -> object:
        """Returns:
            screenshot (numpy array): The image of the environment"""
        pass

    def get_state(self) -> object:
        """Returns
            state (list[float]): The state of the environment"""
        pass
