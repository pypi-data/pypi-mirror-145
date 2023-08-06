"""Parser module to parse gear config.json."""

from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> Path:
    """Parse config.json and return relevant inputs and options."""

    return Path(gear_context.get_input_path("dicom")).resolve()
