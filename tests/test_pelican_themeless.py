#!/usr/bin/env python3

# External dependencies.
import pytest


def test_import_fails() -> None:
    with pytest.raises(NotImplementedError):
        import pelican_themeless
