#!/bin/bash
# scripts/smoke-test.sh
# 執行 smoke test 並驗證基本產出結構
# 用法：bash scripts/smoke-test.sh

set -e

echo "=== Smoke Test 開始 ==="
echo ""

# 1. 確認 fixture 存在
echo "[1/4] 確認 test fixtures..."
MISSING=0
for f in test/csv/google_ads_raw.csv test/csv/meta_ads_raw.csv test/csv/ga4_raw.csv; do
  if [ ! -f "$f" ]; then
    echo "  ✗ 缺少：$f"
    MISSING=1
  else
    echo "  ✓ $f"
  fi
done
if [ "$MISSING" -eq 1 ]; then
  echo ""
  echo "錯誤：缺少必要的 fixture 檔案，請先補齊 test/csv/ 資料後再跑。"
  exit 1
fi

# 2. 跑 combine_to_360_table.py
echo ""
echo "[2/4] 建立 360 table..."
APP_ENV=development python3 scripts/combine_to_360_table.py \
  --google-ads-csv test/csv/google_ads_raw.csv \
  --meta-ads-csv test/csv/meta_ads_raw.csv \
  --ga4-csv test/csv/ga4_raw.csv \
  --out exports/360_table.csv

if [ ! -f "exports/360_table.csv" ]; then
  echo "  ✗ exports/360_table.csv 未產出"
  exit 1
fi
echo "  ✓ exports/360_table.csv 產出成功"

# 3. 跑 period_compare_360_table.py
echo ""
echo "[3/4] 執行 period compare..."
APP_ENV=development python3 scripts/period_compare_360_table.py \
  --input exports/360_table.csv \
  --current-start 2026-05-16 \
  --current-end 2026-05-22 \
  --previous-start 2026-05-08 \
  --previous-end 2026-05-14 \
  --out exports/period_compare.json

if [ ! -f "exports/period_compare.json" ]; then
  echo "  ✗ exports/period_compare.json 未產出"
  exit 1
fi
echo "  ✓ exports/period_compare.json 產出成功"

# 4. 確認 output/ 有 zzz-test- 開頭的檔案（由 Codex 產出，需手動跑完再驗證）
echo ""
echo "[4/4] 確認 output/ 產出..."
TEST_OUTPUT=$(ls output/zzz-test-analysis-*.md 2>/dev/null | tail -1)
if [ -z "$TEST_OUTPUT" ]; then
  echo "  ⚠ output/ 下尚無 zzz-test- 檔案"
  echo "    請先用以下指令讓 Codex 跑完整分析，再重新執行此腳本驗證："
  echo ""
  echo "    codex '$(cat test/smoke-test-prompt.md | head -5)'"
  echo ""
else
  echo "  ✓ 找到：$TEST_OUTPUT"

  # 檢查標題
  FIRST_LINE=$(head -1 "$TEST_OUTPUT")
  if echo "$FIRST_LINE" | grep -q "# This is TEST"; then
    echo "  ✓ 標題包含 TEST 標記"
  else
    echo "  ✗ 標題缺少 TEST 標記，實際內容：$FIRST_LINE"
  fi

  # 檢查必要區塊
  for section in "Observation" "Inference" "Recommendation" "Data gaps" "Routing Result" "Environment Gate Result"; do
    if grep -q "$section" "$TEST_OUTPUT"; then
      echo "  ✓ 包含：$section"
    else
      echo "  ✗ 缺少：$section"
    fi
  done
fi

echo ""
echo "=== Smoke Test 完成 ==="
echo ""
echo "手動驗證項目（需要自己看）："
echo "  - Analysis Trace 裡的 Routing Result 是否與 test/smoke-test-prompt.md 預期一致"
echo "  - 終端機回覆是否只有摘要與路徑，沒有完整分析"
echo "  - Observation / Inference / Recommendation 是否確實三層分離"