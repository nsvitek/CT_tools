#!/usr/bin/env python3
"""
CT scan metadata collector.

Recursively finds .pca and .xtekct files (and the common typo .xtect),
copies them into <INPUT_DIR>/scan_metadata while preserving their relative
folder structure, extracts CT metadata, and writes scan_metadata.csv.

The parser preserves the important fields from the original scripts:
VoxelSize, NumberImages/Projections, Voltage, Current, Filter,
ExposureTime, Avg, Sensitivity, Watts, and Skip.

Usage:
    1. Set INPUT_DIR below and run:
         python collect_ct_metadata.py

    2. Or pass a directory on the command line:
         python collect_ct_metadata.py "D:/path/to/data"
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path
from typing import Dict, Optional, Tuple


# ---------------------------------------------------------------------------
# User configuration
# ---------------------------------------------------------------------------
INPUT_DIR = r"F:/British_Rats/lowprotein_diet_3m"   # <-- Set this, or pass the path on CLI.
OUTPUT_DIR_NAME = "scan_metadata"
CSV_NAME = "scan_metadata.csv"

# The original code uses .xtekct. .xtect is included because it was specified
# in the request and is a common filename typo.
SUPPORTED_SUFFIXES = {".pca", ".xtekct", ".xtect"}


CSV_COLUMNS = [
    "file_name",
    "file_type",
    "source_path",
    "copied_path",
    "voxel_size_x_mm",
    "voxel_size_y_mm",
    "voxel_size_z_mm",
    "number_images",
    "voltage_kv",
    "current_ua",
    "watts",
    "exposure_time_s",
    "filter",
    "avg",
    "sensitivity",
    "skip",
    "parse_status",
    "parse_error",
]


def parse_key_value_file(path: Path) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Read an INI-like CT metadata file without requiring a third-party package.

    Returns:
        values: {"Section.Key": "value", ...}
        sections: {"key": "section"} for convenience.
    """
    values: Dict[str, str] = {}
    sections: Dict[str, str] = {}
    section = ""

    # CT metadata files are normally ASCII/UTF-8. errors="replace" prevents a
    # single unusual byte from stopping an entire batch.
    with path.open("r", encoding="utf-8-sig", errors="replace") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith(("#", ";")):
                continue

            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].strip().lower()
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            values[f"{section}.{key}"] = value
            sections[key] = section

    return values, sections


def get(values: Dict[str, str], section: str, key: str,
        default: Optional[str] = None) -> Optional[str]:
    return values.get(f"{section.lower()}.{key.lower()}", default)


def first(values: Dict[str, str], candidates, default=None):
    """Return the first present key from (section, key) candidates."""
    for section, key in candidates:
        value = get(values, section, key)
        if value not in (None, ""):
            return value
    return default


def as_float(value: Optional[str]):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def watts(voltage, current):
    v = as_float(voltage)
    i = as_float(current)
    if isinstance(v, (int, float)) and isinstance(i, (int, float)):
        return v * i / 1000.0
    return None


def parse_pca(path: Path) -> Dict[str, object]:
    values, _ = parse_key_value_file(path)

    # Original script used one VoxelSize value for X/Y/Z. Modern PCA files
    # generally provide VoxelSizeX/Y; retain all available dimensions.
    vx = first(values, [("geometry", "voxelsizex"), ("geometry", "voxelsize")])
    vy = first(values, [("geometry", "voxelsizey"), ("geometry", "voxelsize")])
    vz = first(values, [("geometry", "voxelsizez"), ("geometry", "voxelsize")])

    number_images = first(values, [
        ("ct", "numberimages"),
        ("acquisition", "numberimages"),
    ])

    voltage = first(values, [("xray", "voltage")])
    current = first(values, [("xray", "current")])
    filter_value = first(values, [
        ("xray", "filter"),
        ("xray", "xrayfilter"),
    ])

    # Preserve the original TimingVal interpretation: milliseconds -> seconds.
    timing_ms = first(values, [("detector", "timingval")])
    exposure_s = as_float(timing_ms)
    if isinstance(exposure_s, (int, float)):
        exposure_s /= 1000.0

    avg = first(values, [
        ("detector", "avg"),
        ("calibimages", "avg"),
        ("calibvalue", "averaging"),
    ])

    sensitivity = first(values, [("detector", "cameragain")])
    # Preserve the original script's special CameraGain mapping.
    if sensitivity == "3":
        sensitivity = "4"

    skip = first(values, [
        ("detector", "skip"),
        ("calibimages", "skip"),
        ("calibvalue", "skip"),
        ("autoco", "skip"),
    ])

    return {
        "voxel_size_x_mm": as_float(vx),
        "voxel_size_y_mm": as_float(vy),
        "voxel_size_z_mm": as_float(vz if vz is not None else vx),
        "number_images": as_float(number_images),
        "voltage_kv": as_float(voltage),
        "current_ua": as_float(current),
        "watts": watts(voltage, current),
        "exposure_time_s": exposure_s,
        "filter": "none" if filter_value == "unknown" else filter_value,
        "avg": as_float(avg),
        "sensitivity": sensitivity,
        "skip": as_float(skip),
    }


def parse_xtekct(path: Path) -> Dict[str, object]:
    values, _ = parse_key_value_file(path)

    vx = first(values, [("xtekct", "voxelsizex")])
    vy = first(values, [("xtekct", "voxelsizey")])
    vz = first(values, [("xtekct", "voxelsizez")])

    voltage = first(values, [("xrays", "xraykv")])
    current = first(values, [("xrays", "xrayua")])

    thickness = first(values, [("ctpro", "filter_thicknessmm")])
    material = first(values, [("ctpro", "filter_material")])

    if thickness is None:
        filter_value = None
    elif thickness == "0.000" or as_float(thickness) == 0:
        filter_value = "none"
    else:
        filter_value = f"{thickness} mm {material or ''}".strip()

    # The original script explicitly reports these as unavailable.
    return {
        "voxel_size_x_mm": as_float(vx),
        "voxel_size_y_mm": as_float(vy),
        "voxel_size_z_mm": as_float(vz),
        "number_images": as_float(first(values, [("xtekct", "projections")])),
        "voltage_kv": as_float(voltage),
        "current_ua": as_float(current),
        "watts": watts(voltage, current),
        "exposure_time_s": "unknown",
        "filter": filter_value,
        "avg": "unknown",
        "sensitivity": "unknown",
        "skip": "unknown",
    }


def extract_metadata(path: Path) -> Dict[str, object]:
    suffix = path.suffix.lower()
    if suffix == ".pca":
        data = parse_pca(path)
    elif suffix in {".xtekct", ".xtect"}:
        data = parse_xtekct(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    return data


def discover_files(input_dir: Path, output_dir: Path):
    """Recursively find supported files, excluding the generated output tree."""
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file():
            continue
        if output_dir in path.parents:
            continue
        if path.suffix.lower() in SUPPORTED_SUFFIXES:
            yield path


def safe_relative_copy(source: Path, input_dir: Path, output_dir: Path) -> Path:
    """Copy while preserving relative paths, preventing filename collisions."""
    relative = source.relative_to(input_dir)
    destination = output_dir / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def process(input_dir: Path) -> Path:
    input_dir = input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {input_dir}")

    output_dir = input_dir / OUTPUT_DIR_NAME
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / CSV_NAME

    files = list(discover_files(input_dir, output_dir))

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()

        for source in files:
            relative_source = source.relative_to(input_dir)
            try:
                copied = safe_relative_copy(source, input_dir, output_dir)
                metadata = extract_metadata(source)

                row = {
                    "file_name": source.name,
                    "file_type": source.suffix.lower().lstrip("."),
                    "source_path": str(relative_source),
                    "copied_path": str(copied.relative_to(output_dir)),
                    **metadata,
                    "parse_status": "OK",
                    "parse_error": "",
                }
            except Exception as exc:
                # Keep one row per file even if one malformed file is present.
                row = {
                    "file_name": source.name,
                    "file_type": source.suffix.lower().lstrip("."),
                    "source_path": str(relative_source),
                    "copied_path": "",
                    "parse_status": "ERROR",
                    "parse_error": f"{type(exc).__name__}: {exc}",
                }
                for key in CSV_COLUMNS:
                    row.setdefault(key, "")

            writer.writerow(row)

    print(f"Found {len(files)} metadata file(s).")
    print(f"Copied files to: {output_dir}")
    print(f"CSV written to:  {csv_path}")
    return csv_path


def main():
    parser = argparse.ArgumentParser(
        description="Collect PCA/XTEKCT CT metadata into scan_metadata."
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        default=INPUT_DIR,
        help="Root directory to search recursively.",
    )
    args = parser.parse_args()

    if args.input_dir == INPUT_DIR and INPUT_DIR == r"C:\path\to\your\data":
        parser.error(
            "Set INPUT_DIR in the script or provide the input directory "
            "as a command-line argument."
        )

    process(Path(args.input_dir))


if __name__ == "__main__":
    main()
