# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2022 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Bytes transform for values that may be optionally present."""

from typing import Any, List, Optional, Tuple

from .dump import Record
from .transform import Transform


class OptionalX(Transform):

    """Bytes transform for values that may be optionally present."""

    def __init__(self, *, fmt: Any, name: Optional[str] = None) -> None:
        if name is None:
            if isinstance(fmt, Transform):
                name = f"Optional[{fmt.name}]"
            else:
                # must be a structure or bitfields
                name = f"Optional[{fmt.__name__}]"

        super().__init__(name)

        self._fmt = fmt

    @property
    def fmt(self) -> Any:
        """Optional format."""
        return self._fmt

    def __pack__(
        self, value: None, pieces: List[bytes], dump: Optional[Record] = None
    ) -> None:
        if value is None:
            if dump is not None:
                dump.value = repr(value)

        else:
            self._fmt.__pack__(value, pieces, dump)

    def __unpack__(
        self, buffer: bytes, offset: int, dump: Optional[Record] = None
    ) -> Tuple[None, int]:
        if buffer[offset:]:
            item, offset = self._fmt.__unpack__(buffer, offset, dump)

        else:
            item = None

            if dump is not None:
                dump.value = "None"

        return item, offset
