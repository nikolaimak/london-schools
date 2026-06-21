# Price Data Pipeline

Scripts to calculate median house prices per MSOA from Land Registry Price Paid data.

## Prerequisites
- Python 3.10+
- `requests` (for postcodes.io API)
- ~200MB disk for raw CSV data

## Pipeline

1. **01_download_data.sh** — Downloads Land Registry Price Paid CSVs (pp-2025.csv, pp-2026.csv)
2. **02_filter_london.py** — Filters to London postcodes only
3. **03_postcode_to_msoa.py** — Maps postcodes to MSOAs via postcodes.io bulk API
4. **04_aggregate_msoa.py** — Calculates median price + sales count per MSOA

## Output
- `london-msoa-prices.json` — 1181 MSOAs with median price and sales count

## Data Source
[Land Registry Price Paid Data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads) — every residential property sale in England & Wales, updated monthly.

## To refresh
```bash
cd scripts
bash 01_download_data.sh
python3 02_filter_london.py
python3 03_postcode_to_msoa.py  # ~10 min (postcodes.io API)
python3 04_aggregate_msoa.py
```
Then copy the output JSON into index.html.
