from .const import configure
from .dumper import QuickDumper, iter_all_dumps, iter_dumps

qd = QuickDumper()
__all__ = ("QuickDumper", "configure", "iter_dumps", "iter_all_dumps", "qd")
