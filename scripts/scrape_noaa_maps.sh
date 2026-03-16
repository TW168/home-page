#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="$PROJECT_ROOT/static/assets/weather"

mkdir -p "$TARGET_DIR"

# Download into temporary files first, then atomically move in place.
TMP_MAX="$TARGET_DIR/MaxT1_conus.png.tmp"
TMP_NATIONAL="$TARGET_DIR/national_forecast.jpg.tmp"

curl -fsSL "https://graphical.weather.gov/images/conus/MaxT1_conus.png" -o "$TMP_MAX"
curl -fsSL "https://www.wpc.ncep.noaa.gov/noaa/national_forecast.jpg" -o "$TMP_NATIONAL"

mv "$TMP_MAX" "$TARGET_DIR/MaxT1_conus.png"
mv "$TMP_NATIONAL" "$TARGET_DIR/national_forecast.jpg"

echo "$(date '+%Y-%m-%d %H:%M:%S') NOAA maps updated in $TARGET_DIR"
