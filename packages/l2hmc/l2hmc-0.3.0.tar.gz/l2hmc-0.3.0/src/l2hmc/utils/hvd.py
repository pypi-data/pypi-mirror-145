"""
hvd.py

Contains dummy class of Horovod methods incase it is uninstalled.
"""

from typing import Any


class Horovod:
    def __init__(self) -> None:
        pass

    def rank(self) -> int:
        return 0

    def local_rank(self) -> int:
        return 0

    def size(self) -> int:
        return 1

    def local_size(self) -> int:
        return 1

    def DistributedGradientTape(self, tape: Any, **kwargs) -> Any:
        return tape

    def broadcast_variables(self, *args, **kwargs) -> None:
        pass
