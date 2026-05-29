# Approval Flow

任何 write action 前必須：

1. Fetch current state。
2. 顯示 proposed change。
3. 說明 expected impact、risk、rollback note。
4. 問使用者是否同意。
5. 只執行被明確同意的改動。

如果使用者只要求分析或建議，保持 read-only，不執行任何帳戶修改。

建立或更新 Google Sheet 報表是 report artifact write，不等於廣告帳戶 write action；但報表內任何建議若會修改 campaign、budget、bid、targeting、creative、tracking、status，仍必須標記 requires approval，並另走 approval flow。
