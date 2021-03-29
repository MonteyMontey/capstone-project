from enum import Enum


class RenderMode(Enum):
    SLOW_RENDER = 1
    FAST_RENDER = 2
    NO_RENDER = 3


def get_dddqn_config(window):
    return [window.ui.learningRateDoubleSpinBoxDDDQN.value(),
            window.ui.gammaDoubleSpinBoxDDDQN.value(),
            window.ui.batchSizeSpinBoxDDDQN.value(),
            window.ui.epsilonDoubleSpinBoxDDDQN.value(),
            window.ui.epsilonDecDoubleSpinBoxDDDQN.value(),
            window.ui.epsilonMinSpinBoxDDDQN.value(),
            window.ui.tauDoubleSpinBoxDDDQN.value(),
            window.ui.layer1SpinBoxDDDQN.value(),
            window.ui.layer2SpinBoxDDDQN.value()]


def get_ddpg_config(window):
    return [window.ui.learningRateAlphaDoubleSpinBoxDDPG.value(),
            window.ui.learningRateBetaDoubleSpinBoxDDPG.value(),
            window.ui.gammaDoubleSpinBoxDDPG.value(),
            window.ui.batchSizeSpinBoxDDPG.value(),
            window.ui.tauDoubleSpinBoxDDPG.value(),
            window.ui.layer1SpinBoxDDPG.value(),
            window.ui.layer2SpinBoxDDPG.value()]


def get_sac_config(window):
    return [window.ui.learningRateAlphaDoubleSpinBoxSAC.value(),
            window.ui.learningRateBetaDoubleSpinBoxSAC.value(),
            window.ui.gammaDoubleSpinBoxSAC.value(),
            window.ui.batchSizeSpinBoxSAC.value(),
            window.ui.tauDoubleSpinBoxSAC.value(),
            window.ui.rewardScaleSpinBoxSAC.value(),
            window.ui.layer1SpinBoxSAC.value(),
            window.ui.layer2spinBoxSAC.value()]


def get_snake_env_config(window):
    grid_size_index = window.ui.gridSizeComboBox.currentIndex()
    grid_size = [5, 7, 9][grid_size_index]

    snake_vision_index = window.ui.snakeVisionComboBox.currentIndex()
    snake_vision = [1, 2, 3, 4][snake_vision_index]

    return grid_size, snake_vision
