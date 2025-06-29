#!/usr/bin/env python3
"""
69交易機器人監控系統 - 主應用
"""
import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# 簡單認證系統
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'mobile': {'password': 'mobile123', 'role': 'mobile'},
    'viewer': {'password': 'view123', 'role': 'viewer'}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username]['password'] == password:
            session['user_id'] = username
            session['role'] = USERS[username]['role']
            return redirect(url_for('dashboard'))
        else:
            flash('用戶名或密碼錯誤')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>69交易監控系統 - 登入</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header text-center">
                            <h4>69交易監控系統</h4>
                        </div>
                        <div class="card-body">
                            <form method="POST">
                                <div class="mb-3">
                                    <label class="form-label">用戶名</label>
                                    <input type="text" class="form-control" name="username" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">密碼</label>
                                    <input type="password" class="form-control" name="password" required>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">登入</button>
                            </form>
                            <div class="mt-3">
                                <small class="text-muted">
                                    三個69股份有限公司版權所有
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    try:
        # 獲取基礎統計
        from dashboard_stats import get_basic_stats, get_recent_signals
        basic_stats = get_basic_stats()
        recent_signals = get_recent_signals(10)
        
        return render_template('dashboard.html', 
                             user=session,
                             basic_stats=basic_stats,
                             recent_signals=recent_signals,
                             last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return f"<h1>監控系統</h1><p>Error: {str(e)}</p><p><a href='/api/sync'>嘗試同步數據</a></p>"

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/sync')
@login_required
def manual_sync():
    try:
        from data_sync import sync_database
        result = sync_database()
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    logger.info("69交易機器人監控系統啟動")
    app.run(host='0.0.0.0', port=5001, debug=False)
