# Budget Pacing Analysis Mode

## 使用情境

使用者詢問預算是否花太快、花不完、月底 pacing、budget allocation、是否 reallocating spend 時使用此 mode。

## 診斷框架

- Compare actual spend vs expected spend for elapsed period.
- Identify campaigns with high spend and poor CPA/ROAS.
- Identify constrained high-efficiency campaigns if impression share / limited by budget data is available.
- Avoid recommending budget changes without approval.
- Treat any budget reallocation as hypothesis unless user explicitly asks for approval workflow.

## 必查資料

- date range and elapsed period
- campaign budget or monthly budget if available
- spend by day and campaign
- conversions, CPA, revenue, ROAS
- impression share / lost IS budget if available for Google Ads
- Meta learning status and edit history if available

## 輸出要求

- Budget pacing summary
- Over-pacing or under-pacing segments
- Reallocation hypothesis
- Risk and rollback note
- Recommended actions marked `requires_approval: true` if they modify budget

若缺少 budget target，只能做 spend distribution analysis，不能判斷 over/under pacing。
