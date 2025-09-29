#!/usr/bin/env python3
"""
Простое Flask приложение для тестирования Railway деплоя
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'KFP Reporting System',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/api/health/')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'KFP Reporting API is running'
    })

@app.route('/api/')
def api():
    return jsonify({
        'message': 'KFP Reporting API',
        'endpoints': {
            'health': '/api/health/',
            'dashboard': '/api/reports/dashboard-stats/',
            'upload': '/api/upload/file/',
            'reports': '/api/reports/'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
