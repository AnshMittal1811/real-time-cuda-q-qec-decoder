from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SurfaceCodeGeometry:
    """Detector-level rotated surface-code geometry used by the prototype."""

    distance: int
    rounds: int

    def __post_init__(self) -> None:
        if self.distance < 3 or self.distance % 2 == 0:
            raise ValueError("distance must be odd and >= 3")
        if self.rounds <= 0:
            raise ValueError("rounds must be positive")

    @property
    def plaquettes_per_round(self) -> int:
        return 2 * self.distance * (self.distance - 1)

    @property
    def syndrome_size(self) -> int:
        return self.plaquettes_per_round * self.rounds

    @property
    def correction_size(self) -> int:
        return 2 * self.distance * self.distance

    def coordinate(self, flat_index: int) -> tuple[int, int, int, int]:
        """Return (round, stabilizer_type, row, col) for a detector index."""

        if flat_index < 0 or flat_index >= self.syndrome_size:
            raise IndexError(flat_index)
        round_id, local = divmod(flat_index, self.plaquettes_per_round)
        stabilizer_type, cell = divmod(local, self.distance * (self.distance - 1))
        row, col = divmod(cell, self.distance)
        return round_id, stabilizer_type, row, col

