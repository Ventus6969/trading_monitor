#!/usr/bin/env python3
"""
查看同步統計和節省情況
"""
import os

STATS_FILE = 'data/.sync_stats'

def show_stats():
    if not os.path.exists(STATS_FILE):
        print("📊 暫無統計數據")
        return
    
    stats = {}
    with open(STATS_FILE, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                stats[key] = value
    
    print("=" * 50)
    print("📊 智能同步統計報告")
    print("=" * 50)
    print(f"總檢查次數: {stats.get('total_checks', 0)}")
    print(f"實際同步次數: {stats.get('actual_syncs', 0)}")
    print(f"節省流量: {stats.get('saved_mb', 0)} MB")
    print(f"最後檢查: {stats.get('last_check', 'N/A')}")
    
    total = int(stats.get('total_checks', 0))
    actual = int(stats.get('actual_syncs', 0))
    if total > 0:
        efficiency = ((total - actual) / total) * 100
        print(f"節省效率: {efficiency:.1f}%")
        
        # 計算費用節省
        saved_mb = float(stats.get('saved_mb', 0))
        saved_cost = saved_mb / 1024 * 0.09  # $0.09 per GB
        print(f"節省費用: ${saved_cost:.2f}")
    print("=" * 50)

if __name__ == '__main__':
    show_stats()
