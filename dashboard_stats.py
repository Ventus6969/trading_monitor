#!/usr/bin/env python3
"""
儀表板統計模組
"""
import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

LOCAL_DB_PATH = "data/trading_signals.db"

def get_db_connection():
    """獲取資料庫連接"""
    if not os.path.exists(LOCAL_DB_PATH):
        # 如果資料庫不存在，嘗試同步
        print("資料庫不存在，嘗試同步...")
        from data_sync import sync_database
        sync_result = sync_database()
        if sync_result['status'] != 'success':
            raise Exception(f"資料庫不存在且同步失敗: {sync_result['message']}")
    
    return sqlite3.connect(LOCAL_DB_PATH)

def get_basic_stats():
    """獲取基礎統計"""
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 檢查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            if 'signals_received' not in tables:
                return get_empty_stats("資料庫表不存在")
            
            # 總信號數
            cursor.execute("SELECT COUNT(*) as total FROM signals_received")
            total_signals = cursor.fetchone()['total']
            
            # 總訂單數
            cursor.execute("SELECT COUNT(*) as total FROM orders_executed")
            total_orders = cursor.fetchone()['total']
            
            # 今日信號
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT COUNT(*) as today_signals 
                FROM signals_received 
                WHERE DATE(datetime(timestamp, 'unixepoch')) = ?
            """, (today,))
            today_signals = cursor.fetchone()['today_signals']
            
            # 總勝率和盈虧
            total_win_rate = 0
            total_pnl = 0
            
            if 'trading_results' in tables:
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_trades,
                        SUM(CASE WHEN is_successful = 1 THEN 1 ELSE 0 END) as successful_trades,
                        SUM(final_pnl) as total_pnl
                    FROM trading_results
                """)
                
                trade_result = cursor.fetchone()
                if trade_result['total_trades'] and trade_result['total_trades'] > 0:
                    total_win_rate = (trade_result['successful_trades'] / trade_result['total_trades']) * 100
                    total_pnl = trade_result['total_pnl'] or 0
            
            # 最近信號時間
            cursor.execute("SELECT MAX(timestamp) as last_signal FROM signals_received")
            last_signal_timestamp = cursor.fetchone()['last_signal']
            
            data_health = 'error'
            last_signal_time = 'N/A'
            
            if last_signal_timestamp:
                last_signal_dt = datetime.fromtimestamp(last_signal_timestamp)
                last_signal_time = last_signal_dt.strftime('%Y-%m-%d %H:%M:%S')
                minutes_ago = (datetime.now() - last_signal_dt).total_seconds() / 60
                
                if minutes_ago < 15:
                    data_health = 'good'
                elif minutes_ago < 60:
                    data_health = 'warning'
            
            return {
                'total_signals': total_signals,
                'total_orders': total_orders,
                'today_signals': today_signals,
                'total_win_rate': round(total_win_rate, 2),
                'week_win_rate': round(total_win_rate, 2),
                'total_pnl': round(total_pnl, 4),
                'avg_pnl': round(total_pnl / max(total_signals, 1), 4),
                'last_signal_time': last_signal_time,
                'active_orders': 0,
                'data_health': data_health
            }
            
    except Exception as e:
        logger.error(f"獲取統計數據錯誤: {str(e)}")
        return get_empty_stats(str(e))

def get_empty_stats(error_msg=""):
    """返回空統計數據"""
    return {
        'total_signals': 0,
        'total_orders': 0,
        'today_signals': 0,
        'total_win_rate': 0,
        'week_win_rate': 0,
        'total_pnl': 0,
        'avg_pnl': 0,
        'last_signal_time': f'錯誤: {error_msg}',
        'active_orders': 0,
        'data_health': 'error'
    }

def get_recent_signals(limit=10):
    """獲取最近信號"""
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    s.*,
                    o.client_order_id,
                    o.status as order_status,
                    r.final_pnl,
                    r.is_successful
                FROM signals_received s
                LEFT JOIN orders_executed o ON s.id = o.signal_id
                LEFT JOIN trading_results r ON o.id = r.order_id
                ORDER BY s.timestamp DESC
                LIMIT ?
            """, (limit,))
            
            signals = []
            for row in cursor.fetchall():
                signal_time = datetime.fromtimestamp(row['timestamp'])
                
                signals.append({
                    'timestamp': signal_time.strftime('%m-%d %H:%M'),
                    'signal_type': row['signal_type'] or 'N/A',
                    'symbol': row['symbol'],
                    'side': row['side'],
                    'atr_value': row['atr_value'],
                    'order_status': row['order_status'] or 'N/A',
                    'final_pnl': row['final_pnl'],
                    'is_successful': row['is_successful']
                })
            
            return signals
            
    except Exception as e:
        logger.error(f"獲取最近信號錯誤: {str(e)}")
        return []
