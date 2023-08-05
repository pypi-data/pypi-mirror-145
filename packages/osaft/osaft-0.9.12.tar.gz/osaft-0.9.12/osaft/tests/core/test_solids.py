import unittest

from osaft.core.frequency import Frequency
from osaft.core.functions import sqrt
from osaft.core.solids import ElasticSolid, RigidSolid
from osaft.tests.basetest import BaseTest


class TestRigidSolid(BaseTest):

    def setUp(self) -> None:

        super().setUp()

        self.cls = RigidSolid(self.f, self.rho_s)
        self.composite_cls = RigidSolid(self.frequency, self.rho_s)
        self.list_cls = [self.cls, self.composite_cls]

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_properties(self):
        self.do_testing(lambda: self.rho_s, lambda: self.cls.rho_s)
        self.do_testing(
            lambda: self.cls.rho_s,
            lambda: self.composite_cls.rho_s,
        )

        self.do_testing(
            lambda: self.f,
            lambda: self.cls.f,
        )
        self.do_testing(
            lambda: self.cls.f,
            lambda: self.composite_cls.f,
        )


class TestElasticSolid(BaseTest):

    def setUp(self) -> None:

        super().setUp()

        self.frequency = Frequency(self.f)
        self.cls = ElasticSolid(self.f, self.E_s, self.nu_s, self.rho_s)
        self.composite_cls = ElasticSolid(
            self.frequency,
            self.E_s, self.nu_s, self.rho_s,
        )
        self.list_cls = [self.cls, self.composite_cls]
    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def compute_B_s(self) -> float:
        return self.E_s / 3 / (1 - 2 * self.nu_s)

    def compute_kappa_s(self) -> float:
        return 3 * (1 - 2 * self.nu_s) / self.E_s

    def compute_c_l(self) -> float:
        return sqrt(
            self.E_s * (1 - self.nu_s)
            / (self.rho_s * (1 + self.nu_s) * (1 - 2 * self.nu_s)),
        )

    def compute_c_t(self) -> float:
        return sqrt(self.E_s / (2 * (1 + self.nu_s) * self.rho_s))

    def compute_k_l(self) -> float:
        omega = self.frequency.omega
        c_l = self.compute_c_l()
        return omega / c_l

    def compute_k_t(self) -> float:
        omega = self.frequency.omega
        c_t = self.compute_c_t()
        return omega / c_t

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_c_l(self) -> None:
        self.do_testing(
            func_1=self.compute_c_l,
            func_2=lambda: self.cls.c_l,
        )
        self.do_testing(
            func_1=self.compute_c_l,
            func_2=lambda: self.composite_cls.c_l,
        )

    def test_c_t(self) -> None:
        self.do_testing(
            func_1=self.compute_c_t,
            func_2=lambda: self.cls.c_t,
        )
        self.do_testing(
            func_1=self.compute_c_t,
            func_2=lambda: self.composite_cls.c_t,
        )

    def test_k_l(self) -> None:
        self.do_testing(
            func_1=self.compute_k_l,
            func_2=lambda: self.cls.k_l,
        )
        self.do_testing(
            func_1=self.compute_k_l,
            func_2=lambda: self.composite_cls.k_l,
        )

    def test_k_t(self) -> None:
        self.do_testing(
            func_1=self.compute_k_t,
            func_2=lambda: self.cls.k_t,
        )
        self.do_testing(
            func_1=self.compute_k_t,
            func_2=lambda: self.composite_cls.k_t,
        )

    def test_kappa_s(self) -> None:
        self.do_testing(
            func_1=self.compute_kappa_s,
            func_2=lambda: self.cls.kappa_s,
        )
        self.do_testing(
            func_1=self.compute_kappa_s,
            func_2=lambda: self.composite_cls.kappa_s,
        )

    def test_B_s(self) -> None:
        self.do_testing(
            func_1=self.compute_B_s,
            func_2=lambda: self.cls.B_s,
        )
        self.do_testing(
            func_1=self.compute_B_s,
            func_2=lambda: self.composite_cls.B_s,
        )


if __name__ == '__main__':
    unittest.main()
