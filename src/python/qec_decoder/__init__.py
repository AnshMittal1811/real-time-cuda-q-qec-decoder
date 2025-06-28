"""Real-time surface-code QEC decoder prototype."""

from qec_decoder.geometry import SurfaceCodeGeometry
from qec_decoder.simulator import SyndromeSample, generate_sample

__all__ = ["SurfaceCodeGeometry", "SyndromeSample", "generate_sample"]

