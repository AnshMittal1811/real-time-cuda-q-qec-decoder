import random
import unittest

from qec_decoder.geometry import SurfaceCodeGeometry
from qec_decoder.simulator import generate_sample


class SimulatorTest(unittest.TestCase):
    def test_generate_sample_is_deterministic_for_seed(self) -> None:
        geometry = SurfaceCodeGeometry(distance=5, rounds=5)
        first = generate_sample(geometry, 0.01, random.Random(11))
        second = generate_sample(geometry, 0.01, random.Random(11))
        self.assertEqual(first, second)
        self.assertEqual(len(first.defects), geometry.syndrome_size)
        self.assertEqual(len(first.correction), geometry.correction_size)


if __name__ == "__main__":
    unittest.main()
