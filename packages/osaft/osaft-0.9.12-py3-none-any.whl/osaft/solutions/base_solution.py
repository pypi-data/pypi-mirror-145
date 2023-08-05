from abc import ABC, abstractmethod

from osaft.core.backgroundfields import WaveType, WrongWaveTypeError


class BaseSolution(ABC):
    """ Base class for all solutions

    :param name: name of the solution
    """

    # supported wave types of the solution
    supported_wavetypes = []

    def __init__(self, name: str):
        self.name = name

    @property
    @abstractmethod
    def wave_type(self) -> WaveType:
        """returns the wave type of the solution"""
        pass

    def check_wave_type(self) -> None:
        """Checks if :attr:`wave_type` is in :attr:`supported_wavetypes`

        :raises WrongWaveTypeError: If :attr:`wave_type` is not supported
        """
        if self.wave_type not in self.supported_wavetypes:
            raise WrongWaveTypeError(
                'Solution does not exist for '
                f'wave_type = {self.wave_type} \n',
                f'supported: {self.supported_wavetypes}',
            )


if __name__ == '__main__':
    pass
