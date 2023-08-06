__author__ = "Filipe Ximenes, Andrey Ilin"
__email__ = "andreyilin@fastmail.com"
__version__ = "3.4.2"


from .adapters import (
    generate_wrapper_from_adapter,
    TapiocaAdapter,
    FormAdapterMixin,
    JSONAdapterMixin,
    XMLAdapterMixin,
)
from .serializers import BaseSerializer, SimpleSerializer, PydanticSerializer


__all__ = (
    "generate_wrapper_from_adapter",
    "TapiocaAdapter",
    "FormAdapterMixin",
    "JSONAdapterMixin",
    "XMLAdapterMixin",
    "BaseSerializer",
    "SimpleSerializer",
    "PydanticSerializer",
)
