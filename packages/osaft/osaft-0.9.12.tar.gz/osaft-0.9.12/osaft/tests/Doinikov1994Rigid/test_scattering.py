import unittest

from osaft import King1934
from osaft.core.functions import SpecialFunctions as Sp
from osaft.core.functions import cos, exp, sin
from osaft.solutions.Doinikov1994Rigid import ScatteringField
from osaft.tests.BaseDoinikov1994.test_base import (
    BaseTestDoinikov1994,
    TestBaseDoinikov1994,
)
from osaft.tests.basetest_scattering import (
    HelperCompareScattering,
    HelperScattering,
)


class TestScattering(BaseTestDoinikov1994, HelperScattering):

    def setUp(self) -> None:
        super().setUp()

        self._v_particle_threshold = 1e-5
        self._v_fluid_threshold = 1e-3
        self.N_max = 2

        self.cls = ScatteringField(
            self.f, self.R_0, self.rho_s,
            self.rho_f, self.c_f,
            self.eta_f, self.zeta_f,
            self.p_0,
            self.wave_type,
            self.position,
            self.N_max,
        )

    def V_r_sc(self, n, r) -> complex:
        # grad(phi)
        out = self.cls.k_f * self.alpha_n(n)
        out *= Sp.d1_hankelh1(n, self.cls.k_f * r)
        # curl(Psi)
        out -= n * (n + 1) / r * self.beta_n(n) * Sp.hankelh1(
            n, self.cls.k_v *
            r,
        )

        out *= self.cls.A_in(n)
        return out

    def V_theta_sc(self, n, r) -> complex:
        # curl(Psi)
        arg_v = self.cls.k_v * r
        out = Sp.hankelh1(n, arg_v)
        out += arg_v * Sp.d1_hankelh1(n, arg_v)
        out *= -self.beta_n(n)
        # grad(phi)
        out += self.alpha_n(n) * Sp.hankelh1(n, self.cls.k_f * r)

        out *= self.cls.A_in(n) / r
        return out

    # ------------------

    def radial_particle_velocity(self, r, theta, t, mode):
        if mode == 1 or mode is None:
            return self.particle_velocity(t) * cos(theta)
        else:
            return 0

    def tangential_particle_velocity(self, r, theta, t, mode):
        if mode == 1 or mode is None:
            return -self.particle_velocity(t) * sin(theta)
        else:
            return 0

    def particle_velocity(self, t):

        out = Sp.besselj(1, self.x)
        out += self.alpha_n(1) * Sp.hankelh1(1, self.x)
        out += 2 * self.beta_n(1) * Sp.hankelh1(1, self.x_v)

        out *= self.cls.A_in(1) * self.cls.k_f * self.rho_t
        out /= self.x

        out *= exp(-1j * self.cls.omega * t)

        return out

    # ------------------
    # generic tests
    # ------------------

    def test_properties(self) -> None:
        properties = ['rho_t', 'mu_1', 'mu_2', 'mu_3', 'mu_4']
        self._test_properties(properties)

    def test_methods_n(self) -> None:
        methods = {}
        methods['alpha_n'] = None
        methods['beta_n'] = None
        methods['xi_n'] = None
        methods['gamma_n'] = None

        self._test_methods_n(methods)

    # ------------------

    def alpha_n(self, n: int) -> complex:
        if n > 1:
            out = n * (n + 1)
            out *= Sp.besselj(n, self.x) * Sp.hankelh1(n, self.x_v)

            out -= self.x * self.gamma_n(n) * Sp.d1_besselj(n, self.x)

            out /= self.xi_n(n)

        elif n > 0:
            out = -2 * (1 - self.rho_t**2) * Sp.besselj(1, self.x)
            out *= Sp.hankelh1(1, self.x_v)

            out -= self.mu_1 * self.mu_3
            out /= self.mu_4

        else:
            out = -Sp.besselj(1, self.x) / Sp.hankelh1(1, self.x)

        return out

    def beta_n(self, n: int) -> complex:
        if n > 1:
            out = Sp.d1_besselj(n, self.x) * Sp.hankelh1(n, self.x)
            out -= Sp.besselj(n, self.x) * Sp.d1_hankelh1(n, self.x)
            out *= -self.x / self.xi_n(n)
        elif n > 0:
            out = self.mu_1 * Sp.hankelh1(1, self.x)
            out -= self.mu_2 * Sp.besselj(1, self.x)
            out *= -(1 - self.rho_t) / self.mu_4
        else:
            out = 0

        return out

    def xi_n(self, n: int) -> complex:
        out = -n * (n + 1)
        out *= Sp.hankelh1(n, self.x)
        out *= Sp.hankelh1(n, self.x_v)

        out += self.x * Sp.d1_hankelh1(n, self.x) * self.gamma_n(n)

        return out

    def gamma_n(self, n: int) -> complex:
        out = self.x_v * Sp.d1_hankelh1(n, self.x_v)
        out += Sp.hankelh1(n, self.x_v)
        return out

    # ------------------

    @property
    def mu_1(self) -> complex:
        out = -self.x * Sp.d1_besselj(1, self.x)
        out += self.rho_t * Sp.besselj(1, self.x)
        return out

    @property
    def mu_2(self) -> complex:
        out = -self.x * Sp.d1_hankelh1(1, self.x)
        out += self.rho_t * Sp.hankelh1(1, self.x)
        return out

    @property
    def mu_3(self) -> complex:
        out = (1 + 2 * self.rho_t)
        out *= Sp.hankelh1(1, self.x_v)

        out += self.x_v * Sp.d1_hankelh1(1, self.x_v)
        return out

    @property
    def mu_4(self) -> complex:
        out = 2 * (1 - self.rho_t**2)
        out *= Sp.hankelh1(1, self.x)
        out *= Sp.hankelh1(1, self.x_v)

        out += self.mu_2 * self.mu_3
        return out


class TestScatteringCompareToKing(
    TestBaseDoinikov1994,
    HelperCompareScattering,
):

    def setUp(self) -> None:
        super().setUp()

        self._scattering_compare_threshold = 1e-2
        self.N_max = 3
        self.eta_f *= 1e-5
        self.zeta_f *= 1e-5
        self.R_0 = 1e-6

        self.cls = ScatteringField(
            self.f,
            self.R_0, self.rho_s,
            self.rho_f, self.c_f, self.eta_f, self.zeta_f,
            self.p_0,
            self.wave_type,
            self.position,
            self.N_max,
        )

        self.compare_cls = King1934.ScatteringField(
            self.f,
            self.R_0, self.rho_s,
            self.rho_f, self.c_f,
            self.p_0,
            self.wave_type,
            self.position,
            self.N_max,
        )


if __name__ == '__main__':
    unittest.main()
