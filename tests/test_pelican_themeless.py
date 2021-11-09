#!/usr/bin/env python3

# Standard libraries.
import importlib
import pathlib
import subprocess
import sys

# External dependencies.
import pytest

_module_spec: importlib.machinery.ModuleSpec = (
    # TODO[mypy issue 4145: Module variable `__spec__` not in type hint.
    #
    # If fixed
    #
    # -   Replace all use of `_module_spec` with `__spec__`.
    # -   Remove import of `importlib.machinery`.
    #
    __spec__  # type: ignore[name-defined]
)


def test_import_fails() -> None:
    with pytest.raises(NotImplementedError):
        # pylint: disable=unused-import
        # pylint: disable=import-outside-toplevel
        import pelican_themeless


def test_minimal_config(tmp_path: pathlib.Path) -> None:
    module_path = pathlib.Path(_module_spec.origin or __file__)
    data_dir = module_path.parent / "minimal_config"

    with subprocess.Popen(
        [sys.executable, "-m", "pelican", "-o", str(tmp_path)],
        cwd=data_dir,
    ) as process:
        try:
            process.communicate(timeout=4)
        except subprocess.TimeoutExpired:
            process.kill()
            raise
    outputs = list(
        out_file
        for out_file in tmp_path.rglob("*")
        if out_file.is_file()
    )
    relative_outputs = sorted(
        out_file.relative_to(tmp_path) for out_file in outputs
    )

    expected_output_dir = data_dir / "output"
    expected_outputs = sorted(
        source.relative_to(expected_output_dir)
        for source in expected_output_dir.rglob("*")
        if source.is_file()
    )
    assert relative_outputs == expected_outputs

    for out_file in relative_outputs:
        assert (tmp_path / out_file).read_text() == (
            expected_output_dir / out_file
        ).read_text()
