from .persistence import Provider
from .filesystem import FilesystemProvider


def provider_factory() -> Provider:
    return FilesystemProvider("./data")
