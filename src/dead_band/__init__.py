from .deadband import apply_deadband as fast_deadband  # type: ignore
from .python_version import apply_deadband as slow_deadband

__all__ = ["slow_deadband", "fast_deadband"]
