"""Main module."""

import logging
import typing as t
import warnings
import zipfile
from pathlib import Path

from fw_file.dicom import DICOMCollection, get_config
from pydicom import config as pydicom_config
from pydicom.datadict import keyword_for_tag

from .fixers import apply_fixers, decode_dcm, is_dcm, standardize_transfer_syntax
from .metadata import add_missing_uid, update_modified_dicom_info

log = logging.getLogger(__name__)

config = get_config()
pydicom_config.settings.reading_validation_mode = pydicom_config.IGNORE


def run(  # pylint: disable=too-many-locals,too-many-branches
    dicom_path: Path, out_dir: Path, transfer_syntax: bool
) -> t.Dict[str, t.List[str]]:
    """Run dicom fixer.

    Args:
        dicom_path (str): Path to directory containing dicom files.
        out_dir (Path): Path to directory to store outputs.
    """
    events = {}
    log.info("Loading dicom")
    updated_transfer_syntax = False
    if zipfile.is_zipfile(str(dicom_path)):
        dcms = DICOMCollection.from_zip(
            dicom_path, filter_fn=is_dcm, force=True, track=True
        )
    else:
        dcms = DICOMCollection(dicom_path, filter_fn=is_dcm, force=True, track=True)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        log.info("Processing dicoms")
        for dcm in dcms:
            filename = dcm.filepath.split("/")[-1]
            decode_dcm(dcm)
            if transfer_syntax:
                updated_transfer_syntax = standardize_transfer_syntax(dcm)
            # Update events from decoding
            dcm_evts = {}
            dcm.tracker.trim()
            for element in dcm.tracker.data_elements:
                if element.events:
                    tagname = str(element.tag).replace(",", "")
                    kw = keyword_for_tag(element.tag)
                    if kw:
                        tagname = kw
                    dcm_evts[tagname] = [str(ev) for ev in element.events]
            fix_evts = apply_fixers(dcm)

            # Handle post-decoding events from fixers (patient sex, incorrect
            # units, etc.)
            for fix in fix_evts:
                if fix.field in dcm_evts:
                    dcm_evts[fix.field].append(repr(fix))
                else:
                    dcm_evts[fix.field] = [repr(fix)]
            if dcm_evts:
                events[filename] = dcm_evts
            update_modified_dicom_info(dcm)
    unique_warnings = handle_warnings(w)
    for msg, count in unique_warnings.items():
        log.warning(f"{msg} x {count} across archive")
    added_uid = add_missing_uid(dcms)

    if (
        (len(events) > 0 and any(len(ev) > 0 for ev in events.values()))
        or added_uid
        or updated_transfer_syntax
    ):
        log.info(f"Writing output to {out_dir / dicom_path.name}")
        if len(dcms) > 1:
            dcms.to_zip(out_dir / dicom_path.name)
        else:
            dcms[0].save(out_dir / dicom_path.name)

    return events


def handle_warnings(
    warning_list: t.List[warnings.WarningMessage],
) -> t.Dict[t.Union[Warning, str], int]:
    """Find unique warnings and their counts from a list of warnings.

    Returns:
        Dictionary of warnings/str as key and int counts as value
    """
    warnings_dict: t.Dict[t.Union[Warning, str], int] = {}
    for warning in warning_list:
        msg = str(warning.message)
        if msg in warnings_dict:
            warnings_dict[msg] += 1
        else:
            warnings_dict[msg] = 1
    return warnings_dict
