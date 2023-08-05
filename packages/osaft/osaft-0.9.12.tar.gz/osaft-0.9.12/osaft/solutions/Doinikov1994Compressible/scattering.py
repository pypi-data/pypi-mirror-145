from typing import Optional, Union

import numpy as np

from osaft.core.backgroundfields import WaveType
from osaft.core.frequency import Frequency
from osaft.core.functions import SpecialFunctions as Sp
from osaft.core.geometries import Sphere
from osaft.core.helper import InputHandler
from osaft.core.variable import ActiveListVariable
from osaft.solutions.BaseDoinikov1994.scattering import (
    BaseScatteringDoinikov1994,
)
from osaft.solutions.Doinikov1994Compressible.coefficientmatrix import (
    CoefficientMatrix,
)


class ScatteringField(CoefficientMatrix, BaseScatteringDoinikov1994):
    """Scattering field of Doinikov (viscous fluid-viscous sphere; 1994)

    :param frequency: Frequency [Hz]
    :param radius: Radius of the solid [m]
    :param rho_s: Density of the fluid-like solid [kg/m^3]
    :param c_s: Speed of sound of the sphere [m/s]
    :param eta_s: shear viscosity of the sphere [Pa s]
    :param zeta_s: bulk viscosity of the sphere [Pa s]
    :param rho_f: Density of the fluid [kg/m^3]
    :param c_f: Speed of sound of the fluid [m/s]
    :param eta_f: shear viscosity [Pa s]
    :param zeta_f: bulk viscosity [Pa s]
    :param p_0: Pressure amplitude of the field [Pa]
    :param position: Position within the standing wave field [m]
    :param wave_type: Type of wave, travel(l)ing or standing
    :param N_max: Highest order mode included in the computation [-]
    """

    def __init__(
        self, frequency: Union[Frequency, float, int],
        radius: Union[Sphere, float, int],
        rho_s: float, c_s: float, eta_s: float, zeta_s: float,
        rho_f: float, c_f: float, eta_f: float, zeta_f: float,
        p_0: float, wave_type: WaveType, position: float,
        N_max: Optional[int] = 5,
    ) -> None:
        """Constructor method
        """

        # init of parent class
        CoefficientMatrix.__init__(
            self,
            frequency=frequency, radius=radius,
            rho_s=rho_s, c_s=c_s, eta_s=eta_s, zeta_s=zeta_s,
            rho_f=rho_f, c_f=c_f, eta_f=eta_f, zeta_f=zeta_f,
            p_0=p_0, wave_type=wave_type, position=position,
        )
        BaseScatteringDoinikov1994.__init__(self, N_max=N_max)

        # Dependent variables
        self._alpha_n = ActiveListVariable(
            self._compute_alpha_n,
            'fluid scattering coefficient alpha_n',
        )
        self._beta_n = ActiveListVariable(
            self._compute_beta_n,
            'fluid scattering coefficient beta_n',
        )
        self._alpha_hat_n = ActiveListVariable(
            self._compute_alpha_hat_n,
            'sphere scattering coefficient alpha_hat_n',
        )
        self._beta_hat_n = ActiveListVariable(
            self._compute_beta_hat_n,
            'sphere scattering coefficient beta_hat_n',
        )

    def __repr__(self):  # pragma: no cover
        return (
            f'Doinikov1994Compressible.ScatteringFiels(frequency={self.f}, '
            f'radius={self.R_0}, '
            f'rho_s={self.rho_s}, c_s={self.c_s}, '
            f'eta_s={self.eta_s}, zeta_s={self.zeta_s}, '
            f'rho_f={self.rho_f}, c_f={self.c_f}, '
            f'eta_f={self.eta_f}, zeta_f={self.zeta_f}, '
            f'p_0={self.p_0}, position={self.position}, {self.wave_type}, '
            f'N_max={self.N_max})'
        )

    # -----------------------------------------------------
    # Scattering coefficients fluid
    # -----------------------------------------------------

    def alpha_n(self, n: int) -> complex:
        """ coefficient :math:`\\alpha_n` (3.13) and (3.20)

        :param n: order
        """
        return self._alpha_n.item(n)

    def _compute_alpha_n(self, n: int) -> complex:
        # computation according to (3.13), (3.14) and (3.20)
        if n == 0:
            tmp1 = 4 * (self.eta_f - self.eta_s) * self.x * self.x_hat
            tmp1 *= Sp.besselj(1, self.x_hat)

            tmp2 = 1j * self.omega * self.R_0**2

            # numerator
            num = self.rho_f * self.x_hat
            num *= Sp.besselj(0, self.x) * Sp.besselj(1, self.x_hat)

            num -= self.rho_s * self.x * (
                Sp.besselj(1, self.x) *
                Sp.besselj(0, self.x_hat)
            )

            num *= tmp2

            num -= tmp1 * Sp.besselj(1, self.x)

            # denominator
            den = self.rho_s * self.x
            den *= Sp.hankelh1(1, self.x) * Sp.besselj(0, self.x_hat)

            den -= self.rho_f * self.x_hat * (
                Sp.hankelh1(0, self.x) *
                Sp.besselj(1, self.x_hat)
            )

            den *= tmp2

            den += tmp1 * Sp.hankelh1(1, self.x)

            new_value = num / den
        else:
            new_value = self.det_M_n(n, 0) / self.det_M_n(n)

        return new_value

    def beta_n(self, n: int) -> complex:
        """ coefficient :math:`\\beta_n` (3.13) and (3.20)

        :param n: order
        """
        return self._beta_n.item(n)

    def _compute_beta_n(self, n: int) -> complex:
        # computation according to (3.13), (3.15) and (3.21)
        if n == 0:
            return 0
        else:
            return self.det_M_n(n, 1) / self.det_M_n(n)

    # -----------------------------------------------------
    # Scattering coefficients sphere
    # -----------------------------------------------------

    def alpha_hat_n(self, n: int) -> complex:
        """ coefficient :math:`\\alpha_hat_n` (3.13) and (3.20)

        :param n: order
        """
        return self._alpha_hat_n.item(n)

    def _compute_alpha_hat_n(self, n: int) -> complex:
        # computation according to (3.13), (3.14) and (3.20)

        if n == 0:
            tmp1 = 4 * (self.eta_f - self.eta_s) * self.x * self.x_hat
            tmp2 = 1j * self.omega * self.R_0**2

            # numerator
            num = Sp.besselj(0, self.x) * Sp.hankelh1(1, self.x)

            num -= Sp.besselj(1, self.x) * Sp.hankelh1(0, self.x)

            num *= tmp2 * self.x * self.rho_f

            # denominator
            den = self.rho_s * self.x
            den *= Sp.hankelh1(1, self.x) * Sp.besselj(0, self.x_hat)

            den -= self.rho_f * self.x_hat * (
                Sp.hankelh1(0, self.x) *
                Sp.besselj(1, self.x_hat)
            )

            den *= tmp2

            den += tmp1 * (
                Sp.hankelh1(1, self.x) *
                Sp.besselj(1, self.x_hat)
            )

            new_value = num / den
        else:
            new_value = self.det_M_n(n, 2) / self.det_M_n(n)
        return new_value

    def beta_hat_n(self, n: int) -> complex:
        """ coefficient :math:`\\beta_hat_n` (3.13) and (3.20)

        :param n: order
        """
        return self._beta_hat_n.item(n)

    def _compute_beta_hat_n(self, n: int) -> complex:
        # computation according to (3.13), (3.15) and (3.21)
        if n == 0:
            return 0
        else:
            return self.det_M_n(n, 3) / self.det_M_n(n)

    # -----------------------------------------------------
    # Methods
    # -----------------------------------------------------

    def radial_particle_velocity(
        self,
        r: Union[float, np.ndarray, list[float]],
        theta: Union[float, np.ndarray, list[float]],
        t: Union[float, np.ndarray, list[float]],
        mode: Optional[int] = None,
    ) -> complex:
        """Particle velocity in radial direction

        Returns the value of the particle velocity
        in radial direction in [m/s]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific modenumber of interest; if `None` then all
                     modes until :attr:`.N_max`
        """
        r, theta, t = InputHandler.handle_input(
            r, theta, t, self.R_0,
            inside_sphere=True,
        )

        def radial_velocity(n: int, r: float) -> complex:
            out = self.k_s * self.alpha_hat_n(n)
            out *= Sp.d1_besselj(n, r * self.k_s)

            arg = r * self.k_vs
            out -= n * (n + 1) / r * self.beta_hat_n(n) * Sp.besselj(n, arg)
            out *= self.A_in(n)
            return out

        out = self.radial_mode_superposition(
            radial_velocity, r, theta, t, mode,
        )

        return out

    def tangential_particle_velocity(
            self,
            r: Union[float, np.ndarray, list[float]],
            theta: Union[float, np.ndarray, list[float]],
            t: Union[float, np.ndarray, list[float]],
            mode: Optional[int] = None,
    ) -> complex:
        """Particle velocity in tangential direction

        Returns the value of the particle velocity
        in tangential direction in [m/s]

        :param r: radial coordinate [m]
        :param theta: tangential coordinate [rad]
        :param t: time [s]
        :param mode: specific modenumber of interest; if `None` then all
                     modes until :attr:`.N_max`
        """
        r, theta, t = InputHandler.handle_input(
            r, theta, t, self.R_0,
            inside_sphere=True,
        )

        def tangential_velocity(n: int, r: float) -> complex:
            out = Sp.besselj(n, self.k_vs * r)
            out += r * self.k_vs * Sp.d1_besselj(n, self.k_vs * r)
            out *= -self.beta_hat_n(n)
            out += self.alpha_hat_n(n) * Sp.besselj(n, self.k_s * r)
            out *= self.A_in(n) / r
            return out

        out = self.tangential_mode_superposition(
            tangential_velocity, r, theta, t, mode,
        )

        return out


if __name__ == '__main__':
    pass
