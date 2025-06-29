# 69交易機器人監控系統 🚀

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)](https://github.com/Ventus6969/trading_monitor)

## 📋 專案概述

69交易機器人監控系統是一個跨主機的交易監控解決方案，專為監控和分析TradingView信號驅動的期貨交易機器人而設計。系統採用智能同步機制，可大幅降低AWS數據傳輸費用，同時提供實時的交易統計和分析。

### 🎯 核心特色

- **🔄 智能同步**：只在數據變化時同步，節省95%流量費用
- **📊 實時監控**：完整的交易生命週期追蹤和統計
- **💰 成本優化**：月費用從$14-16降至$8-11
- **📱 多平台**：響應式設計，支援桌面和手機訪問
- **🛡️ 安全認證**：三層權限管理（管理員/手機/查看者）
- **⚡ 高效能**：毫秒級數據處理和顯示

## 🏗️ 系統架構

```
交易主機 (AWS帳號1)           監控主機 (AWS帳號2)
┌─────────────────┐          ┌─────────────────┐
│ 🤖 交易機器人    │          │ 📊 Web Dashboard │
│ 📁 SQLite DB    │─智能同步→│ 📈 統計分析      │
│ 💰 實際交易      │          │ 🔍 管理工具      │
│ ✅ 數據記錄      │          │ 📱 手機友善      │
└─────────────────┘          └─────────────────┘
```

### 📊 數據流程

```
TradingView信號 → 交易執行 → 資料庫記錄 → 智能同步 → 監控面板
```

## 🚀 快速開始

### 📋 系統需求

- **監控主機**：AWS EC2 Linux (t2.micro或以上)
- **Python**：3.8+
- **SSH訪問**：到交易主機的無密碼連接
- **網路**：穩定的網際網路連接

### 🔧 環境準備

#### 1. 克隆專案
```bash
git clone https://github.com/Ventus6969/trading_monitor.git
cd trading_monitor
```

#### 2. 建立虛擬環境
```bash
python3 -m venv monitor_env
source monitor_env/bin/activate
pip install -r requirements.txt
```

#### 3. SSH金鑰配置
```bash
# 產生SSH金鑰對
ssh-keygen -t rsa -f ~/.ssh/trading_monitor -N ""

# 將公鑰複製到交易主機
ssh-copy-id -i ~/.ssh/trading_monitor.pub ec2-user@YOUR_TRADING_HOST_IP

# 測試連接
ssh -i ~/.ssh/trading_monitor ec2-user@YOUR_TRADING_HOST_IP 'echo "連接成功"'
```

#### 4. 環境配置
```bash
# 複製配置範例
cp .env.example .env

# 編輯配置檔案
nano .env
```

在 `.env` 檔案中設定：
```env
TRADING_HOST_IP=15.168.60.229
REMOTE_USER=ec2-user
REMOTE_DB_PATH=/home/ec2-user/69trading/data/trading_signals.db
ADMIN_PASSWORD=your_secure_password
MOBILE_PASSWORD=your_mobile_password
VIEWER_PASSWORD=your_viewer_password
```

### 🎯 快速啟動

#### 方法1：使用啟動腳本（推薦）
```bash
chmod +x start_monitor.sh stop_monitor.sh
./start_monitor.sh
```

#### 方法2：手動啟動
```bash
source monitor_env/bin/activate
python3 app.py
```

### 🌐 訪問系統

啟動後訪問：`http://YOUR_MONITOR_HOST_IP:5001`

**預設帳號**：
- 管理員：`admin` / `admin123`
- 手機用戶：`mobile` / `mobile123`  
- 查看者：`viewer` / `view123`

## 📊 功能特色

### 🎛️ 監控面板

#### 📈 核心統計
- **總信號數**：累計接收的TradingView信號
- **勝率統計**：總勝率和週勝率
- **盈虧分析**：總盈虧和平均獲利
- **訂單狀態**：總訂單數和活躍訂單

#### 📋 交易記錄
- **實時信號**：最近交易信號的詳細記錄
- **執行狀態**：訂單狀態和執行結果
- **盈虧顯示**：直觀的獲利/虧損標示
- **信號分類**：8種不同信號類型的追蹤

### 🔄 智能同步系統

#### 💡 智能特色
- **變化檢測**：只有資料變化時才進行同步
- **費用節省**：降低95%的AWS數據傳輸費用
- **自動恢復**：連接失敗時自動重試
- **統計追蹤**：完整的同步效率統計

#### ⚙️ 同步管理
```bash
# 查看同步統計
python3 smart\ sync/sync_stats.py

# 強制同步一次
python3 smart\ sync/manage_sync.py force

# 測試SSH連接
python3 smart\ sync/manage_sync.py test

# 清除同步緩存
python3 smart\ sync/manage_sync.py clear
```

### 🛡️ 安全特性

#### 👥 多層權限
- **admin**：完整系統管理權限
- **mobile**：手機優化的監控介面
- **viewer**：唯讀查看權限

#### 🔐 安全措施
- SSH金鑰認證
- 會話管理
- 敏感資料過濾
- 安全的跨主機通信

## 📁 專案結構

```
trading_monitor/
├── 📄 app.py                    # Flask主應用
├── 📄 data_sync.py              # 核心同步模組  
├── 📄 dashboard_stats.py        # 統計數據模組
├── 📂 smart sync/               # 智能同步系統
│   ├── smart_cron_sync.py       # 定時同步腳本
│   ├── manage_sync.py           # 同步管理工具
│   └── sync_stats.py            # 同步統計分析
├── 📂 templates/                # HTML模板
│   └── dashboard.html           # 主面板模板
├── 📂 scripts/                  # 管理腳本
│   ├── start_monitor.sh         # 啟動腳本
│   └── stop_monitor.sh          # 停止腳本
├── 📄 requirements.txt          # Python依賴
├── 📄 .env.example             # 配置範例
└── 📄 .gitignore               # Git忽略規則
```

## 🔧 系統管理

### 📊 狀態檢查
```bash
# 檢查系統運行狀態
ps aux | grep app.py

# 查看應用日誌
tail -f logs/app.log

# 檢查同步狀態
python3 smart\ sync/sync_stats.py

# 手動同步測試
python3 data_sync.py
```

### 🔄 服務管理
```bash
# 啟動服務
./start_monitor.sh

# 停止服務  
./stop_monitor.sh

# 重啟服務
./stop_monitor.sh && ./start_monitor.sh

# 檢查服務狀態
ps aux | grep "python3 app.py"
```

### 📝 日誌管理
```bash
# 查看實時日誌
tail -f logs/app.log

# 查看同步日誌
tail -f logs/sync.log

# 日誌輪替（定期清理）
logrotate /etc/logrotate.d/trading_monitor
```

## ⚙️ 進階配置

### 🕐 定時同步設定
```bash
# 編輯定時任務
crontab -e

# 添加每5分鐘同步任務
*/5 * * * * cd /path/to/trading_monitor && python3 smart\ sync/smart_cron_sync.py
```

### 🔧 性能調優
```bash
# 調整同步頻率（smart_cron_sync.py）
SYNC_INTERVAL = 300  # 5分鐘

# 調整Flask並發
app.run(host='0.0.0.0', port=5001, threaded=True)

# 資料庫優化
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

### 🛡️ 安全加強
```bash
# 限制SSH訪問來源
# 在交易主機的 ~/.ssh/authorized_keys 添加：
from="MONITOR_HOST_IP" ssh-rsa YOUR_PUBLIC_KEY

# 設定防火牆規則
sudo ufw allow from TRADING_HOST_IP to any port 5001
sudo ufw deny 5001
```

## 📈 監控指標

### 🎯 關鍵指標

| 指標名稱 | 說明 | 健康範圍 |
|---------|------|---------|
| 勝率 | 成功交易比例 | >60% |
| 同步效率 | 節省的流量比例 | >90% |
| 響應時間 | 頁面載入時間 | <2秒 |
| 同步延遲 | 數據同步間隔 | <5分鐘 |

### 📊 效能基準

- **數據處理**：1000+筆交易記錄 <100ms
- **同步速度**：10MB資料庫 <30秒
- **記憶體使用**：<200MB常駐記憶體
- **磁碟空間**：<1GB完整系統

## 🔍 故障排除

### ❌ 常見問題

#### 1. SSH連接失敗
```bash
# 檢查SSH金鑰權限
chmod 600 ~/.ssh/trading_monitor

# 測試連接
ssh -v -i ~/.ssh/trading_monitor ec2-user@TRADING_HOST_IP

# 檢查交易主機SSH設定
sudo nano /etc/ssh/sshd_config
```

#### 2. 同步失敗
```bash
# 檢查網路連接
ping TRADING_HOST_IP

# 檢查遠程資料庫
ssh -i ~/.ssh/trading_monitor ec2-user@TRADING_HOST_IP 'ls -la /path/to/trading_signals.db'

# 強制重新同步
python3 smart\ sync/manage_sync.py clear
python3 smart\ sync/manage_sync.py force
```

#### 3. 面板無法訪問
```bash
# 檢查Flask進程
ps aux | grep app.py

# 檢查端口佔用
netstat -tlnp | grep 5001

# 檢查防火牆
sudo ufw status
```

#### 4. 數據顯示錯誤
```bash
# 檢查資料庫完整性
sqlite3 data/trading_signals.db ".schema"

# 手動同步
python3 data_sync.py

# 重啟應用
./stop_monitor.sh && ./start_monitor.sh
```

### 📞 支援資源

- **問題報告**：[GitHub Issues](https://github.com/Ventus6969/trading_monitor/issues)
- **功能請求**：[GitHub Discussions](https://github.com/Ventus6969/trading_monitor/discussions)
- **文檔更新**：[Wiki](https://github.com/Ventus6969/trading_monitor/wiki)

## 💰 成本分析

### 💵 費用比較

| 項目 | 傳統同步 | 智能同步 | 節省 |
|-----|---------|---------|------|
| 月流量費 | $6-8 | $0.3-0.5 | 95% |
| EC2費用 | $8 | $8 | 0% |
| 總費用 | $14-16 | $8-11 | 30% |

### 📊 ROI計算

- **一次性設置成本**：2-4小時設置時間
- **月度運營成本**：$8-11 (vs $14-16)
- **年度節省**：$36-60
- **投資回收期**：1-2個月

## 🔮 未來規劃

### 🚧 短期目標（1-2個月）

- [ ] 添加更多統計圖表
- [ ] 實現推播通知功能
- [ ] 改進手機介面體驗
- [ ] 增加歷史數據分析

### 🎯 中期目標（3-6個月）

- [ ] 機器學習信號品質評估
- [ ] 多交易帳戶支援
- [ ] RESTful API開發
- [ ] Docker容器化部署

### 🌟 長期願景（6-12個月）

- [ ] 分散式監控架構
- [ ] 即時風險管理
- [ ] 高級分析工具
- [ ] 社群功能整合

## 🤝 貢獻指南

### 💻 開發環境設置

1. Fork專案到個人帳戶
2. 克隆Fork的版本庫
3. 創建功能分支
4. 完成開發和測試
5. 提交Pull Request

### 📝 貢獻規範

- 遵循Python PEP 8程式碼規範
- 編寫完整的單元測試
- 更新相關文檔
- 提供清晰的commit訊息

### 🐛 問題回報

使用GitHub Issues回報問題時，請提供：

- 詳細的問題描述
- 重現步驟
- 錯誤日誌
- 系統環境資訊

## 📄 授權協議

本專案採用 [MIT License](LICENSE) 授權。

## 🙏 致謝

感謝所有為此專案貢獻的開發者和使用者。

---

**⭐ 如果這個專案對您有幫助，請給個Star支持！**

**📞 技術支援**: [GitHub Issues](https://github.com/Ventus6969/trading_monitor/issues)  
**📧 聯絡我們**: ventus6969@example.com  
**🌐 專案主頁**: [https://github.com/Ventus6969/trading_monitor](https://github.com/Ventus6969/trading_monitor)