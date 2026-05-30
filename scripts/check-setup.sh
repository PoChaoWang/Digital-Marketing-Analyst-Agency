#!/bin/bash
# scripts/check-setup.sh
# 偵測現有設定狀態，輸出 YAML 供 /ma-start 讀取
# 用法：bash scripts/check-setup.sh

check_field() {
  local file="$1"
  local key="$2"
  if grep -qE "^${key}=.+" "$file" 2>/dev/null; then
    echo "filled"
  else
    echo "empty"
  fi
}

check_section() {
  local file="$1"
  local section="$2"
  # 找到 section 標題後，看下一個非空白行是否有內容
  if awk "/^## ${section}/{found=1; next} found && /^## /{exit} found && /[^[:space:]]/{print; exit}" "$file" 2>/dev/null | grep -q "."; then
    echo "filled"
  else
    echo "empty"
  fi
}

echo "# check-setup output"
echo "# generated: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# --- .env ---
echo "env:"
if [ -f ".env" ]; then
  echo "  exists: true"
  echo "  fields:"
  for key in \
    APP_ENV \
    DATA_SOURCE_CONFIG \
    GOOGLE_ADS_CLIENT_ID \
    GOOGLE_ADS_CLIENT_SECRET \
    GOOGLE_ADS_DEVELOPER_TOKEN \
    GOOGLE_ADS_REFRESH_TOKEN \
    GOOGLE_ADS_LOGIN_CUSTOMER_ID \
    GOOGLE_ADS_CUSTOMER_ID \
    META_APP_ID \
    META_APP_SECRET \
    META_ACCESS_TOKEN \
    META_AD_ACCOUNT_ID \
    META_BUSINESS_ID \
    GA4_PROPERTY_ID \
    GA4_CREDENTIALS_JSON \
    GA4_CLIENT_EMAIL \
    GA4_PRIVATE_KEY \
    GA4_CLIENT_ID \
    GA4_CLIENT_SECRET \
    GA4_REFRESH_TOKEN; do
    echo "    ${key}: $(check_field .env $key)"
  done
else
  echo "  exists: false"
  echo "  fields: ~"
fi

echo ""

# --- accounts.yml ---
echo "accounts_yml:"
if [ -f "config/accounts.yml" ]; then
  echo "  exists: true"
else
  echo "  exists: false"
fi

echo ""

# --- business_context ---
echo "business_context:"
if [ -f "profile/business-context.md" ]; then
  echo "  exists: true"
  echo "  sections:"
  echo "    brand: $(check_section profile/business-context.md Brand)"
  echo "    kpi: $(check_section profile/business-context.md KPI)"
  echo "    client_priorities: $(check_section profile/business-context.md 'Client Priorities')"
else
  echo "  exists: false"
  echo "  sections: ~"
fi