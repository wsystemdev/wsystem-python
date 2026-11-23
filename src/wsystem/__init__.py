"""W System API client: EU VAT (VIES), EORI, company registers, sanctions, KYB and EU e-invoicing (EN 16931, XRechnung, ZUGFeRD / Factur-X, Peppol)."""
__version__ = "0.1.0"

from .client import DEFAULT_BASE_URL, WSystem, decode_pdf  # noqa: E402
from ._generated import OPERATIONS  # noqa: E402
from ._http import RequestOptions  # noqa: E402
from .errors import (  # noqa: E402
    APIConnectionError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ConflictError,
    NotFoundError, PaymentRequiredError, RateLimitError, ServerError, WSystemError,
)

__all__ = ["WSystem", "OPERATIONS", "RequestOptions", "decode_pdf", "DEFAULT_BASE_URL", "__version__", "WSystemError", "APIConnectionError",
           "APITimeoutError", "APIStatusError", "BadRequestError", "AuthenticationError", "PaymentRequiredError", "NotFoundError",
           "ConflictError", "RateLimitError", "ServerError"]
