#!/bin/bash
# 69交易機器人監控系統啟動腳本

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 啟動69交易機器人監控系統${NC}"

# 檢查是否在正確目錄
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ 錯誤：請在trading_monitor目錄下執行此腳本${NC}"
    exit 1
fi

# 創建必要目錄
mkdir -p logs data

# 檢查虛擬環境
if [ ! -d "monitor_env" ]; then
    echo -e "${YELLOW}⚠️  虛擬環境不存在，正在創建...${NC}"
    python3 -m venv monitor_env
    source monitor_env/bin/activate
    pip install -r requirements.txt
else
    echo -e "${GREEN}✅ 啟動虛擬環境${NC}"
    source monitor_env/bin/activate
fi

# 檢查是否已在運行
if pgrep -f "python3 app.py" > /dev/null; then
    echo -e "${YELLOW}⚠️  監控系統已在運行中${NC}"
    echo "如需重啟，請先執行: ./stop_monitor.sh"
    exit 1
fi

# 檢查SSH連接
echo -e "${YELLOW}🔍 檢查SSH連接...${NC}"
if python3 -c "from data_sync import check_remote_db_exists; print('SSH連接正常' if check_remote_db_exists() else 'SSH連接失敗')"; then
    echo -e "${GREEN}✅ SSH連接正常${NC}"
else
    echo -e "${RED}❌ SSH連接失敗，請檢查配置${NC}"
fi

# 啟動應用
echo -e "${GREEN}🎯 啟動Flask應用...${NC}"
nohup python3 app.py > logs/app.log 2>&1 &

# 獲取PID
APP_PID=$!
echo $APP_PID > .app.pid

# 等待啟動
sleep 3

# 檢查是否成功啟動
if ps -p $APP_PID > /dev/null; then
    echo -e "${GREEN}✅ 監控系統啟動成功！${NC}"
    echo -e "${GREEN}📊 Dashboard地址: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'localhost'):5001${NC}"
    echo -e "${GREEN}📝 日誌位置: logs/app.log${NC}"
    echo -e "${GREEN}🔧 停止服務: ./stop_monitor.sh${NC}"
else
    echo -e "${RED}❌ 啟動失敗，請檢查logs/app.log${NC}"
    exit 1
fi