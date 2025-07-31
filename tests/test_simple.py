#!/usr/bin/env python3
"""
간단한 API 테스트 스크립트
web3 의존성 없이 기본 API 기능을 테스트합니다.
"""

import sys
import json
import pytest
from app import create_app

@pytest.fixture
def app():
    """Flask 앱 fixture"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """테스트 클라이언트 fixture"""
    return app.test_client()

def test_health_check(client):
    """헬스체크 테스트"""
    response = client.get('/health')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['status'] == 'healthy'
    assert result['service'] == 'zk-nft'

def test_index(client):
    """루트 엔드포인트 테스트"""
    response = client.get('/')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['message'] == 'zk-nft API 서버'
    assert 'endpoints' in result

def test_bank_credit_criteria(client):
    """은행 신용등급 기준 조회 테스트"""
    response = client.get('/api/bank/credit-criteria')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['bank_id'] == 'BANK_001'
    assert 'criteria' in result

def test_external_credit_inquiry(client):
    """외부기관 신용정보 조회 테스트"""
    data = {
        'customer_id': 'CUST_001',
        'customer_name': '김철수',
        'requested_amount': 10000000,
        'purpose': '사업자금',
        'request_id': 'REQ_TEST_001',
        'customer_address': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6'
    }
    
    response = client.post('/api/external/credit-inquiry',
                         data=json.dumps(data),
                         content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'inquiry_id' in result
    assert 'credit_score' in result
    assert 'credit_grade' in result

def test_external_generate_proof(client):
    """외부기관 ZK-Proof 생성 테스트"""
    data = {
        'inquiry_id': 'INQ_TEST_001',
        'customer_id': 'CUST_001',
        'credit_score': 750,
        'credit_grade': 'B',
        'max_loan_amount': 50000000
    }
    
    response = client.post('/api/external/generate-proof',
                         data=json.dumps(data),
                         content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['status'] == 'generated'
    assert 'proof_id' in result
    assert 'proof_data' in result

def test_external_mint_nft(client):
    """외부기관 NFT 발행 테스트"""
    data = {
        'proof_id': 'PROOF_TEST_001',
        'customer_id': 'CUST_001',
        'credit_grade': 'B',
        'max_loan_amount': 50000000,
        'customer_address': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6'
    }
    
    response = client.post('/api/external/mint-nft',
                         data=json.dumps(data),
                         content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['status'] == 'minted'
    assert 'token_id' in result
    assert 'nft_metadata' in result

def test_customer_get_nft_info(client):
    """고객 NFT 정보 조회 테스트"""
    token_id = 'NFT_TEST_001'
    
    response = client.get(f'/api/customer/nft/{token_id}')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['token_id'] == token_id
    assert 'attributes' in result

def test_customer_get_nfts(client):
    """고객 NFT 목록 조회 테스트"""
    customer_address = '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6'
    
    response = client.get(f'/api/customer/my-nfts/{customer_address}')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['customer_address'] == customer_address
    assert 'nfts' in result
    assert isinstance(result['nfts'], list)

# 기존 main 함수는 유지 (별도 실행용)
def main():
    """메인 테스트 함수 (별도 실행용)"""
    print("🎯 zk-nft API 테스트 시작")
    print("=" * 50)
    
    # Flask 앱 생성
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        # 테스트 실행
        tests = [
            test_health_check,
            test_index,
            test_bank_credit_criteria,
            test_external_credit_inquiry,
            test_external_generate_proof,
            test_external_mint_nft,
            test_customer_get_nft_info,
            test_customer_get_nfts
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                test(client)
                passed += 1
                print(f"✅ {test.__name__} 통과")
            except Exception as e:
                print(f"❌ {test.__name__} 실패: {e}")
        
        print("=" * 50)
        print(f"📊 테스트 결과: {passed}/{total} 통과")
        
        if passed == total:
            print("🎉 모든 테스트가 통과했습니다!")
            return True
        else:
            print("⚠️ 일부 테스트가 실패했습니다.")
            return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 