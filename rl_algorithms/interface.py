import numpy as np


class AlgInterface:
    """The interface defines the methods which each algorithm class needs to implement"""

    def choose_action(self, observation: list) -> np.ndarray:
        """Chooses an action based on the state aka observation of an environment"""
        pass

    def remember(self, state: list, action: object, reward: float, state_: list, done: bool) -> None:
        """Inserts the state, the action, the reward, the new state, and done into the replay memory

        Args:
            state (List): The state of the environment before the action was executed.
            action (Object): The action that was executed.
            reward (float): The reward given for the executed action.
            state_ (list): The state of the environment after the action was executed.
            done (bool): Whether action lead to the failing the environment"""
        pass

    def learn(self) -> None:
        """Samples a batch of memories from the replay buffer and fits the neural network to it"""
        pass
