# Climate Data Pipeline

## Purpose
Process IMD daily gridded rainfall and temperature data for the climate digital twin project.

## Temperature Processing

**Source:** India Meteorological Department (IMD)

- Tmax: `data/raw/tmax/`
- Tmin: `data/raw/tmin/`
- Period: 2015–2025
- Native resolution: 1° × 1°
- Original format: binary `.GRD` files
- Output format: NetCDF (`.nc`)

### Processing steps
1. Read the raw binary files as little-endian float32 values.
2. Validate that each file contains the expected number of daily grid values.
3. Reshape the data to time, latitude and longitude dimensions.
4. Convert the IMD missing-value marker `99.9` to `NaN`.
5. Select the Maharashtra bounding box: latitude 15.5°–22.1°N and longitude 72.6°–80.9°E.
6. Export the processed data and validity mask to NetCDF.

### Outputs
- `data/processed/tmax_c_2015_2025.nc`
- `data/processed/tmin_c_2015_2025.nc`

Each output contains 4,018 daily records and a 7 × 8 grid.

## Scripts
- `inspect_data.py` — inspect rainfall NetCDF data.
- `validate_rainfall.py` — validate rainfall date continuity.
- `inspect_temperature_binary.py` — inspect raw temperature binary data.
- `process_temperature.py` — process Tmax and Tmin data.
- `verify_temperature.py` — verify processed temperature outputs.
- `check_mask_consistency.py` — inspect rainfall missing-cell patterns; confirm its current behavior before relying on it.

## Important Notes
- Raw input files should remain unchanged.
- Missing values must not be replaced with zero.
- Temperature data remains on its native 1° grid; no interpolation is performed.
- The spatial subset is a rectangular bounding box, not an exact Maharashtra state-boundary mask.
- Temperature mask consistency has been validated against raw Tmax and Tmin data for all years from 2015 through 2025 within the selected Maharashtra bounding box.
