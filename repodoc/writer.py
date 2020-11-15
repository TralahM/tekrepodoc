"""Repodoc Template Writer module."""
import os
import logging

logger = logging.getLogger("repodoc")


def prepare_destination(
    out_path,
    base_path=os.path.abspath(os.path.curdir),
    logger=logger,
):
    """Prepare Output Destination Path if subfolders dont exist create them."""
    fullpath = os.path.join(base_path, out_path)
    dirname = os.path.dirname(fullpath)
    os.makedirs(dirname, exist_ok=True)
    logger.debug(f"Prepared Destination Path: {fullpath}.")
    return fullpath


def write_rendered_template(
    out_path,
    content,
    base_path=os.path.abspath(os.path.curdir),
    logger=logger,
):
    """Write content to output filepath."""
    prepped_path = prepare_destination(out_path, base_path=base_path)
    with open(prepped_path, "w") as wf:
        wf.write(content)
    logger.info(f"Written {out_path}.")
