def _setup():
    from colorama import init

    init()


_setup()

from colorama import *  # pyright: ignore[reportWildcardImportFromLibrary] # noqa: F403, E402
