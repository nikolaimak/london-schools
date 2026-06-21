#!/bin/bash
# Download Price Paid data for 2025 and 2026
set -e

echo "Downloading 2025 Price Paid data..."
curl -L -o /tmp/pp-2025.csv "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2025.csv" --progress-bar

echo "Downloading 2026 Price Paid data..."
curl -L -o /tmp/pp-2026.csv "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2026.csv" --progress-bar

echo "Done. File sizes:"
ls -lh /tmp/pp-2025.csv /tmp/pp-2026.csv
