#!/usr/bin/env python3
"""
zk-nft: Zero-Knowledge Proof 기반 신용등급 NFT 시스템
메인 Flask 애플리케이션
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def create_app():
    """Flask 애플리케이션 팩토리 함수"""
    app = Flask(__name__)
    
    # CORS 설정
    CORS(app)
    
    # 설정 로드
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['BLOCKCHAIN_URL'] = os.getenv('BLOCKCHAIN_URL', 'http://localhost:8545')
    app.config['CONTRACT_ADDRESS'] = os.getenv('CONTRACT_ADDRESS', '0x0000000000000000000000000000000000000000')
    
    # API 블루프린트 등록
    from api.bank import bank_bp
    from api.external import external_bp
    from api.customer import customer_bp
    
    app.register_blueprint(bank_bp, url_prefix='/api/bank')
    app.register_blueprint(external_bp, url_prefix='/api/external')
    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    
    # 헬스체크 엔드포인트
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'zk-nft',
            'version': '1.0.0'
        })
    
    # 루트 엔드포인트
    @app.route('/')
    def index():
        return jsonify({
            'message': 'zk-nft API 서버',
            'description': 'Zero-Knowledge Proof 기반 신용등급 NFT 시스템',
            'endpoints': {
                'health': '/health',
                'bank': '/api/bank',
                'external': '/api/external',
                'customer': '/api/customer'
            }
        })
    
    # 에러 핸들러
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 zk-nft 서버 시작 중...")
    print(f"📍 서버 주소: http://{host}:{port}")
    print(f"🔧 디버그 모드: {debug}")
    
    app.run(host=host, port=port, debug=debug) 