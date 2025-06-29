#!/usr/bin/env python3
"""
數據同步模組
"""
import os
import subprocess
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# 配置（請修改為你的實際配置）
REMOTE_HOST = "15.168.60.229"  # 你的交易主機IP
REMOTE_USER = "ec2-user"
REMOTE_DB_PATH = "/home/ec2-user/69trading/data/trading_signals.db"
LOCAL_DB_PATH = "data/trading_signals.db"
SSH_KEY_PATH = os.path.expanduser("~/.ssh/trading_monitor")

def sync_database():
    """同步資料庫"""
    try:
        # 確保目錄存在
        os.makedirs(os.path.dirname(LOCAL_DB_PATH), exist_ok=True)
        
        # 檢查SSH連接
        print("測試SSH連接...")
        test_cmd = [
            'ssh', '-i', SSH_KEY_PATH,
            '-o', 'ConnectTimeout=10',
            '-o', 'StrictHostKeyChecking=no',
            f'{REMOTE_USER}@{REMOTE_HOST}',
            'echo "SSH test successful"'
        ]
        
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return {'status': 'error', 'message': f'SSH連接失敗: {result.stderr}'}
        
        print("SSH連接成功，開始同步資料庫...")
        
        # 同步資料庫檔案
        scp_cmd = [
            'scp', '-i', SSH_KEY_PATH,
            '-o', 'ConnectTimeout=10',
            '-o', 'StrictHostKeyChecking=no',
            f'{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_DB_PATH}',
            LOCAL_DB_PATH
        ]
        
        result = subprocess.run(scp_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            file_size = os.path.getsize(LOCAL_DB_PATH) if os.path.exists(LOCAL_DB_PATH) else 0
            logger.info(f"資料庫同步成功，檔案大小: {file_size} bytes")
            return {
                'status': 'success', 
                'message': f'同步成功，檔案大小: {file_size} bytes',
                'timestamp': datetime.now().isoformat()
            }
        else:
            logger.error(f"SCP同步失敗: {result.stderr}")
            return {'status': 'error', 'message': f'同步失敗: {result.stderr}'}
            
    except Exception as e:
        logger.error(f"同步過程出錯: {str(e)}")
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("開始數據同步...")
    result = sync_database()
    if result['status'] == 'success':
        print(f"✓ 同步成功: {result['message']}")
    else:
        print(f"✗ 同步失敗: {result['message']}")
