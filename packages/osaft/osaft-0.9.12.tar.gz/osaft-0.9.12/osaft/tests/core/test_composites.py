import unittest

from osaft.core.basecomposite import (
    BaseFrequencyComposite,
    BaseSphereFrequencyComposite,
)
from osaft.core.frequency import Frequency
from osaft.core.functions import pi
from osaft.core.geometries import Sphere
from osaft.tests.basetest import BaseTest


class TestBaseFrequencyComposite(BaseTest):

    def test_types_for_frequency(self):
        cls = BaseFrequencyComposite(10.1)
        self.assertTrue(isinstance(cls, BaseFrequencyComposite))
        cls = BaseFrequencyComposite(10.1)
        self.assertTrue(isinstance(cls, BaseFrequencyComposite))

        F = Frequency(1e6)
        cls = BaseFrequencyComposite(F)
        self.assertTrue(isinstance(cls, BaseFrequencyComposite))

    def test_TypeError(self):

        self.assertRaises(TypeError, BaseFrequencyComposite, 's')


class TestBaseSphereFrequencyComposite(BaseTest):

    def test_types_for_sphere(self):
        cls = BaseSphereFrequencyComposite(10.1, 10)
        self.assertTrue(isinstance(cls, BaseSphereFrequencyComposite))
        cls = BaseSphereFrequencyComposite(10.1, 10.0)
        self.assertTrue(isinstance(cls, BaseSphereFrequencyComposite))

        S = Sphere(1e-6)
        cls = BaseSphereFrequencyComposite(10.1, S)
        self.assertTrue(isinstance(cls, BaseSphereFrequencyComposite))

    def test_properties(self):
        def V(R):
            return 4 / 3 * R**3 * pi

        def A(R):
            return 4 * R**2 * pi

        R = 1e-6
        f = 1e6
        cls = BaseSphereFrequencyComposite(f, R)

        self.assertAlmostEqual(R, cls.R_0)
        self.assertAlmostEqual(V(R), cls.V)
        self.assertAlmostEqual(A(R), cls.A)

        R = 4.39e-6
        cls.R_0 = R
        self.assertAlmostEqual(R, cls.R_0)
        self.assertAlmostEqual(V(R), cls.V)
        self.assertAlmostEqual(A(R), cls.A)

    def test_TypeError(self):
        self.assertRaises(
            TypeError, BaseSphereFrequencyComposite,
            10.0, 's',
        )


if __name__ == '__main__':
    unittest.main()
