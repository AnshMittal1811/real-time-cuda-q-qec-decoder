import unittest

from qec_decoder.geometry import SurfaceCodeGeometry


class SurfaceCodeGeometryTest(unittest.TestCase):
    def test_surface_code_geometry_sizes(self) -> None:
        geometry = SurfaceCodeGeometry(distance=5, rounds=3)
        self.assertEqual(geometry.plaquettes_per_round, 40)
        self.assertEqual(geometry.syndrome_size, 120)
        self.assertEqual(geometry.correction_size, 50)
        self.assertEqual(geometry.coordinate(0), (0, 0, 0, 0))

    def test_surface_code_geometry_rejects_invalid_distance(self) -> None:
        with self.assertRaises(ValueError):
            SurfaceCodeGeometry(distance=4, rounds=3)


if __name__ == "__main__":
    unittest.main()
