# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2022 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test OptionalX transform properties."""

import pytest
from plum.exceptions import SizeError
from plum.littleendian import uint8
from plum.optional import OptionalX
from plum.structure import Structure, member


class Sample(Structure):

    member1: int = member(fmt=uint8)


class Test:

    optional_x = OptionalX(fmt=uint8)

    def test_default_name_transform(self):
        assert self.optional_x.name == "Optional[uint8]"

    def test_default_name_structure(self):
        assert OptionalX(fmt=Sample).name == "Optional[Sample]"

    def test_fmt(self):
        assert self.optional_x.fmt is uint8

    def test_explicit_name(self):
        assert OptionalX(fmt=uint8, name="Optional").name == "Optional"

    def test_nbytes(self):
        with pytest.raises(SizeError):
            self.optional_x.nbytes  # pylint: disable=pointless-statement
