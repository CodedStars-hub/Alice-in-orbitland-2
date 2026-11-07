"""Typed failures shared by future scientific modules."""


class InvalidScientificInput(ValueError):
    """An input violates a scientific contract."""


class UnsupportedCoordinateConvention(InvalidScientificInput):
    """A coordinate convention or frame is unsupported."""


class MissingScientificData(RuntimeError):
    """Required scientific inputs are unavailable."""


class IncompleteScientificCoverage(MissingScientificData):
    """Available inputs do not cover the requested scientific domain."""


class UnsupportedTemporalCoverage(IncompleteScientificCoverage):
    """Inputs do not cover the requested time interval."""


class ScientificComputationFailure(RuntimeError):
    """A scientific computation could not complete."""


class NumericalConvergenceFailure(ScientificComputationFailure):
    """A numerical method failed its declared convergence policy."""
