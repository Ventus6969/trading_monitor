#!/usr/bin/env python3
"""
智能定時同步 - 只有檢測到變化才同步
可以節省90%以上的流量費用
"""
import os
import hashlib
import subprocess
import logging
from datetime import datetime
from data_sync import sync_database

# 設置簡單日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置文件
REMOTE_HOST = "15.168.60.229"
REMOTE_USER = "ec2-user"
REMOTE_DB_PATH = "/home/ec2-user/69trading/data/trading_signals.db"
SSH_KEY_PATH = os.path.expanduser("~/.ssh/trading_monitor")
HASH_FILE = 'data/.last_sync_hash'
STATS_FILE = 'data/.sync_stats'

def get_remote_file_info():
    """獲取遠程文件信息（大小和雜湊值）"""
    try:
        # 獲取文件大小和雜湊值
        cmd = [
            'ssh', '-i', SSH_KEY_PATH,
            '-o', 'ConnectTimeout=5',
            '-o', 'StrictHostKeyChecking=no',
            f'{REMOTE_USER}@{REMOTE_HOST}',
            f'if [ -f {REMOTE_DB_PATH} ]; then stat -c%s {REMOTE_DB_PATH} && md5sum {REMOTE_DB_PATH}; else echo "0"; echo "none none"; fi'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                size = int(lines[0])
                hash_value = lines[1].split()[0] if len(lines[1].split()) > 0 else "none"
                return size, hash_value
        return 0, None
    except Exception as e:
        logger.error(f"獲取遠程文件信息失敗: {str(e)}")
        return 0, None

def get_local_file_info():
    """獲取本地文件信息"""
    local_db = 'data/trading_signals.db'
    if not os.path.exists(local_db):
        return 0, None
    
    try:
        size = os.path.getsize(local_db)
        with open(local_db, 'rb') as f:
            hash_value = hashlib.md5(f.read()).hexdigest()
        return size, hash_value
    except:
        return 0, None

def read_last_sync_info():
    """讀取上次同步信息"""
    if not os.path.exists(HASH_FILE):
        return None, 0
    
    try:
        with open(HASH_FILE, 'r') as f:
            content = f.read().strip()
            if '|' in content:
                hash_value, size = content.split('|')
                return hash_value, int(size)
            else:
                return content, 0
    except:
        return None, 0

def save_sync_info(hash_value, size):
    """保存同步信息"""
    try:
        os.makedirs(os.path.dirname(HASH_FILE), exist_ok=True)
        with open(HASH_FILE, 'w') as f:
            f.write(f"{hash_value}|{size}")
    except Exception as e:
        logger.error(f"保存同步信息失敗: {str(e)}")

def update_sync_stats(synced=False, saved_mb=0):
    """更新同步統計"""
    try:
        stats = {'total_checks': 0, 'actual_syncs': 0, 'saved_mb': 0, 'last_check': ''}
        
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if '=' in line:
                        key, value = line.strip().split('=')
                        if key in ['total_checks', 'actual_syncs']:
                            stats[key] = int(value)
                        elif key == 'saved_mb':
                            stats[key] = float(value)
                        else:
                            stats[key] = value
        
        stats['total_checks'] += 1
        if synced:
            stats['actual_syncs'] += 1
        else:
            stats['saved_mb'] += saved_mb
        stats['last_check'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(STATS_FILE, 'w') as f:
            for key, value in stats.items():
                f.write(f"{key}={value}\n")
                
        # 計算節省比例
        if stats['total_checks'] > 0:
            efficiency = ((stats['total_checks'] - stats['actual_syncs']) / stats['total_checks']) * 100
            logger.info(f"同步效率: {efficiency:.1f}% (已節省 {stats['saved_mb']:.1f}MB 流量)")
            
    except Exception as e:
        logger.error(f"更新統計失敗: {str(e)}")

def main():
    """主要邏輯"""
    logger.info("🔍 檢查遠程數據是否有變化...")
    
    # 獲取文件信息
    remote_size, remote_hash = get_remote_file_info()
    local_size, local_hash = get_local_file_info()
    last_hash, last_size = read_last_sync_info()
    
    logger.info(f"遠程文件: {remote_size} bytes, hash: {remote_hash[:8] if remote_hash else 'None'}...")
    logger.info(f"本地文件: {local_size} bytes, hash: {local_hash[:8] if local_hash else 'None'}...")
    
    # 判斷是否需要同步
    need_sync = False
    reason = ""
    
    if remote_hash is None:
        logger.warning("⚠️  無法獲取遠程文件信息，跳過同步")
        update_sync_stats(synced=False, saved_mb=0)
        return
    
    if remote_hash == "none" or remote_size == 0:
        logger.info("📊 遠程資料庫為空，跳過同步")
        update_sync_stats(synced=False, saved_mb=0)
        return
    
    if local_hash is None:
        need_sync = True
        reason = "本地無資料庫文件"
    elif remote_hash != last_hash:
        need_sync = True
        reason = "遠程數據已更新"
    elif remote_size != last_size:
        need_sync = True
        reason = "文件大小已變化"
    
    if need_sync:
        logger.info(f"🔄 {reason}，開始同步...")
        result = sync_database()
        
        if result['status'] == 'success':
            save_sync_info(remote_hash, remote_size)
            logger.info("✅ 同步完成")
            update_sync_stats(synced=True)
        else:
            logger.error(f"❌ 同步失敗: {result['message']}")
            update_sync_stats(synced=False, saved_mb=0)
    else:
        # 估算節省的流量
        saved_mb = remote_size / 1024 / 1024
        logger.info(f"📊 數據無變化，跳過同步 (節省 {saved_mb:.2f}MB 流量)")
        update_sync_stats(synced=False, saved_mb=saved_mb)

if __name__ == '__main__':
    main()
