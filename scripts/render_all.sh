#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

examples=(
  "examples/sales-dashboard/sales-dashboard.qmd"
  "examples/pdf-briefing/pdf-briefing.qmd"
  "examples/pdf-briefing-extended/pdf-briefing-extended.qmd"
  "examples/pdf-briefing-extended-altair/pdf-briefing-extended-altair.qmd"
)

for doc in "${examples[@]}"; do
  echo "Rendering ${doc}"
  quarto render "${ROOT}/${doc}"
done

echo "Rendering PowerPoint deck"
quarto render "${ROOT}/examples/ppt-deck/ppt-deck.qmd" --to pptx

echo "All documents rendered."
