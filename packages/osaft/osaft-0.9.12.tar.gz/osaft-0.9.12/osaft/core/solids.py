from typing import Union

from osaft import log
from osaft.core.basecomposite import BaseFrequencyComposite
from osaft.core.frequency import Frequency
from osaft.core.functions import sqrt
from osaft.core.variable import ActiveVariable, PassiveVariable


class RigidSolid(BaseFrequencyComposite):
    """RigidSolid class

    :param frequency: excitation frequency in [Hz]
    :param rho: density in [kg/m^3]
    """

    def __init__(
        self, frequency: Union[int, float, Frequency],
        rho: float,
    ) -> None:
        """Constructor method
        """

        # Calling parent class
        super().__init__(frequency)

        # Independent variables
        self._rho_s = PassiveVariable(rho, 'density rho')

        if type(self) is RigidSolid:
            log.debug(f'Creating {self}')

    def __repr__(self) -> str:
        return f'RigidSolid(f={self.f}, rho={self.rho_s})'

    # -------------------------------------------------------------------------
    # Setters and Getters for Independent Variables
    # -------------------------------------------------------------------------

    @property
    def rho_s(self) -> float:
        """Density of the solid :math:`\\rho_{s}`.

        :getter: returns the value for the density
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._rho_s.value

    @rho_s.setter
    def rho_s(self, value: float) -> None:
        self._rho_s.value = value


class ElasticSolid(RigidSolid):
    """ElasticSolid class

    :param frequency: excitation frequency in [Hz]
    :param E: Young's modulus in [Pa]
    :param nu: Poisson's ratio in [-]
    :param rho: density in [km m^-3]
    """

    def __init__(self, frequency, E, nu, rho) -> None:
        """Constructor method
        """

        super().__init__(frequency, rho)

        # Independent variables
        self._E_s = PassiveVariable(E, "Young's modulus E")
        self._nu_s = PassiveVariable(nu, "Poisson's ratio nu")

        # Dependent variables
        self._c_l = ActiveVariable(self._compute_c_l, 'primary wave speed c_l')
        self._k_l = ActiveVariable(
            self._compute_k_l,
            'wavenumber of primary wave k_l',
        )

        self._c_t = ActiveVariable(
            self._compute_c_t,
            'secondary wave speed c_t',
        )
        self._k_t = ActiveVariable(
            self._compute_k_t,
            'wavenumber of secondary wave k_t',
        )

        self._B_s = ActiveVariable(self._compute_B_s, 'bulk modulus B_s')
        self._kappa_s = ActiveVariable(
            self._compute_kappa_s,
            'compressibility kappa_s',
        )

        # Dependencies
        self._c_l.is_computed_by(self._E_s, self._nu_s, self._rho_s)
        self._k_l.is_computed_by(self._c_l, self.frequency._omega)

        self._c_t.is_computed_by(self._E_s, self._nu_s, self._rho_s)
        self._k_t.is_computed_by(self._c_t, self.frequency._omega)

        self._B_s.is_computed_by(self._E_s, self._nu_s)
        self._kappa_s.is_computed_by(self._B_s)

        # no if clause neede because last in inheritance diagram
        log.debug(f'Creating {self}')

    def __repr__(self) -> str:
        return (
            f'ElasticSolid(f={self.f}, rho={self.rho_s}, '
            f'E={self.E_s}, nu={self.nu_s})'
        )

    # -------------------------------------------------------------------------
    # Setters and Getters for Independent Variables
    # -------------------------------------------------------------------------

    @property
    def E_s(self) -> float:
        """Young's modulus of the solid :math:`E_{s}` [Pa].

        :getter: returns the value for the Young's modulus
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._E_s.value

    @E_s.setter
    def E_s(self, value: float) -> None:
        self._E_s.value = value

    @property
    def nu_s(self) -> float:
        """Poisson's ratio of the solid :math:`\\nu_{s}`.

        :getter: returns the value for the Poisson's ratio
        :setter: automatically invokes
            :meth:`osaft.core.variable.BaseVariable.notify`
        """
        return self._nu_s.value

    @nu_s.setter
    def nu_s(self, value: float) -> None:
        self._nu_s.value = value

    # -------------------------------------------------------------------------
    # Getters for Dependent Variables
    # -------------------------------------------------------------------------

    @property
    def B_s(self) -> float:
        """Returns the bulk modulus of the solid :math:`B_{s}` [Pa]
        """
        return self._B_s.value

    @property
    def kappa_s(self) -> float:
        """Returns the compressibility of the solid :math:`\\kappa_{s}` [1/Pa]
        """
        return self._kappa_s.value

    @property
    def c_l(self) -> float:
        """Returns the longitudinal wave speed in the solid :math:`c_l` [m/s]
        """
        return self._c_l.value

    @property
    def c_t(self) -> float:
        """Return the transverse wave speed in the solid :math:`c_t` [m/s]
        """
        return self._c_t.value

    @property
    def k_l(self) -> float:
        """Returns the longitudinal wave number in the solid :math:`k_l` [1/m]
        """
        return self._k_l.value

    @property
    def k_t(self) -> float:
        """Returns the transverse wave number in the solid :math:`k_t` [1/m]
        """
        return self._k_t.value

    # -------------------------------------------------------------------------
    # Dependent Variables Methods
    # -------------------------------------------------------------------------

    def _compute_B_s(self) -> float:
        return self.E_s / (1 - 2 * self.nu_s) / 3

    def _compute_kappa_s(self) -> float:
        return 1 / self.B_s

    def _compute_c_l(self) -> float:
        return sqrt(
            self.E_s * (1 - self.nu_s) / (
                self.rho_s * (1 + self.nu_s)
                * (1 - 2 * self.nu_s)
            ),
        )

    def _compute_c_t(self) -> float:
        return sqrt(self.E_s / (2 * (1 + self.nu_s) * self.rho_s))

    def _compute_k_l(self) -> float:
        return self.omega / self.c_l

    def _compute_k_t(self) -> float:
        return self.omega / self.c_t


if __name__ == '__main__':
    pass
