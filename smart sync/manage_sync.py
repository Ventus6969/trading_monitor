#!/usr/bin/env python3
"""
同步管理工具
"""
import os
import sys
import subprocess

def force_sync():
    """強制同步一次"""
    print("🔄 強制執行同步...")
    from data_sync import sync_database
    result = sync_database()
    print(f"結果: {result['message']}")

def clear_cache():
    """清除同步緩存"""
    files_to_remove = ['data/.last_sync_hash', 'data/.sync_stats']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"✅ 已刪除 {file}")
    print("🔄 緩存已清除，下次檢查將強制同步")

def test_connection():
    """測試SSH連接"""
    print("🔍 測試SSH連接...")
    cmd = ['ssh', '-i', os.path.expanduser('~/.ssh/trading_monitor'),
           '-o', 'ConnectTimeout=5', 'ec2-user@15.168.60.229', 'echo "連接成功"']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ SSH連接正常")
        else:
            print(f"❌ SSH連接失敗: {result.stderr}")
    except Exception as e:
        print(f"❌ 連接測試出錯: {str(e)}")

def show_help():
    print("🛠️  同步管理工具")
    print("用法: python3 manage_sync.py [選項]")
    print()
    print("選項:")
    print("  stats    - 查看同步統計")
    print("  force    - 強制同步一次")
    print("  clear    - 清除同步緩存")
    print("  test     - 測試SSH連接")
    print("  help     - 顯示此幫助")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == 'stats':
        os.system('python3 sync_stats.py')
    elif sys.argv[1] == 'force':
        force_sync()
    elif sys.argv[1] == 'clear':
        clear_cache()
    elif sys.argv[1] == 'test':
        test_connection()
    elif sys.argv[1] == 'help':
        show_help()
    else:
        print(f"未知選項: {sys.argv[1]}")
        show_help()
