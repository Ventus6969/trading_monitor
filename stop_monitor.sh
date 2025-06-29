#!binbash
# 69交易機器人監控系統停止腳本

# 顏色定義
RED='033[0;31m'
GREEN='033[0;32m'
YELLOW='033[1;33m'
NC='033[0m' # No Color

echo -e ${RED}🛑 停止69交易機器人監控系統${NC}

# 方法1：通過PID檔案停止
if [ -f .app.pid ]; then
    PID=$(cat .app.pid)
    if ps -p $PID  devnull; then
        echo -e ${YELLOW}🔍 找到進程 PID $PID${NC}
        kill $PID
        sleep 2
        
        if ps -p $PID  devnull; then
            echo -e ${RED}⚠️  正常停止失敗，強制終止...${NC}
            kill -9 $PID
        fi
        
        rm -f .app.pid
        echo -e ${GREEN}✅ 監控系統已停止${NC}
    else
        echo -e ${YELLOW}⚠️  PID檔案存在但進程不存在${NC}
        rm -f .app.pid
    fi
else
    echo -e ${YELLOW}⚠️  未找到PID檔案，嘗試其他方式...${NC}
fi

# 方法2：通過進程名稱停止
APP_PIDS=$(pgrep -f python3 app.py)
if [ ! -z $APP_PIDS ]; then
    echo -e ${YELLOW}🔍 找到app.py進程 $APP_PIDS${NC}
    killall -f python3 app.py 2devnull
    sleep 1
    
    # 檢查是否還在運行
    if pgrep -f python3 app.py  devnull; then
        echo -e ${RED}⚠️  強制終止...${NC}
        killall -9 -f python3 app.py 2devnull
    fi
    
    echo -e ${GREEN}✅ 所有app.py進程已停止${NC}
else
    echo -e ${GREEN}ℹ️  沒有發現運行中的監控系統${NC}
fi

# 清理
rm -f .app.pid

echo -e ${GREEN}🎯 系統已完全停止${NC}