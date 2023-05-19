class SpekulatioError(Exception):
    """Base exeption for Spekulatio errors."""

    pass


class SpekulatioInternalError(SpekulatioError):
    """Irrecoverable and inconsistent state found during execution."""

    pass

class SpekulatioConfigError(SpekulatioError):
    """Configuration error detected in user provided data."""

    pass
