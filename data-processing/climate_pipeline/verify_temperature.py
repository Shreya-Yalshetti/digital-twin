
from pathlib import Path

import numpy as np
import xarray as xr

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

CONFIGS = [
    ("tmax", "Maxtemp_MaxT_", "tmax_c"),
    ("tmin", "Mintemp_MinT_", "tmin_c"),
]

MISSING_VALUE = 99.9

# The output grid coordinates must match the processing script.
LAT_START, LAT_END = 8, 15
LON_START, LON_END = 6, 14

all_passed = True

for folder, prefix, variable in CONFIGS:
    output_path = PROCESSED_DIR / f"{variable}_2015_2025.nc"

    with xr.open_dataset(output_path) as dataset:
        print(f"\nChecking {variable}")

        for year in range(2015, 2026):
            days = 366 if __import__("calendar").isleap(year) else 365
            raw_path = RAW_DIR / folder / f"{prefix}{year}.GRD"

            raw = np.fromfile(raw_path, dtype="<f4")

            if raw.size != days * 31 * 31:
                print(f"{year}: FAIL — unexpected raw file size")
                all_passed = False
                continue

            raw = raw.reshape(days, 31, 31)
            raw_subset = raw[:, LAT_START:LAT_END, LON_START:LON_END]

            expected_mask = ~np.isclose(raw_subset, MISSING_VALUE)

            saved = dataset.sel(time=str(year))
            actual_mask = saved["valid_mask"].values.astype(bool)

            matches = np.array_equal(expected_mask, actual_mask)
            temperature = saved[variable].values

            # Valid raw observations must be finite; missing observations must be NaN.
            values_correct = (
                np.isfinite(temperature[expected_mask]).all()
                and np.isnan(temperature[~expected_mask]).all()
            )

            passed = matches and values_correct
            all_passed = all_passed and passed

            print(
                f"{year}: {'PASS' if passed else 'FAIL'} | "
                f"mask_match={matches} | "
                f"raw_missing={(~expected_mask).sum()} | "
                f"output_missing={np.isnan(temperature).sum()}"
            )

print("\nOverall result:", "PASS" if all_passed else "FAIL")
