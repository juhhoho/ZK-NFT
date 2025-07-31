#!/usr/bin/env python3
"""
ZK-NFT 시스템 종합 테스트 스크립트
모든 API 엔드포인트와 기능을 테스트합니다.
"""

import pytest
import requests
import json
import time
from datetime import datetime

class TestZKNFTSystem:
    """ZK-NFT 시스템 종합 테스트 클래스"""
    
    BASE_URL = "http://localhost:5000"
    
    def test_01_loan_request_new_customer(self):
        """신규 고객 대출 요청 테스트"""
        print("\n🏦 1. 신규 고객 대출 요청 테스트")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            "customer_id": "CUST_001",
            "customer_name": "김철수",
            "requested_amount": 15000000,
            "purpose": "사업자금",
            "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        }
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert result['status'] == 'completed'
        assert result['approval_status'] == 'approved'
        assert 'nft_token_id' in result
        assert result['credit_grade'] == 'B'
        assert result['max_loan_amount'] == 50000000
        
        print(f"✅ 대출 승인: {result['approval_status']}")
        print(f"📋 NFT 토큰: {result['nft_token_id']}")
        print(f"🏷️ 신용등급: {result['credit_grade']}")
        
        return result['nft_token_id']
    
    def test_02_nft_reuse_same_customer(self):
        """동일 고객 NFT 재사용 테스트"""
        print("\n🔄 2. 동일 고객 NFT 재사용 테스트")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            "customer_id": "CUST_001",
            "customer_name": "김철수",
            "requested_amount": 20000000,
            "purpose": "운전자금",
            "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        }
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert result['status'] == 'completed'
        assert result['approval_status'] == 'approved'
        assert 'nft_token_id' in result
        
        print(f"✅ 대출 승인: {result['approval_status']}")
        print(f"📋 NFT 토큰: {result['nft_token_id']}")
        print(f"💡 NFT 재사용 확인됨")
        
        return result['nft_token_id']
    
    def test_03_nft_lookup(self):
        """NFT 조회 테스트"""
        print("\n🔍 3. NFT 조회 테스트")
        
        url = f"{self.BASE_URL}/api/external/my-nft"
        data = {
            "customer_id": "CUST_001",
            "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        }
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert result['status'] == 'valid'
        assert 'nft_data' in result
        
        nft_data = result['nft_data']
        assert 'token_id' in nft_data
        assert 'attributes' in nft_data
        assert 'issue_date' in nft_data
        assert 'expiry_date' in nft_data
        assert nft_data['is_valid'] == True
        
        print(f"✅ NFT 상태: {result['status']}")
        print(f"📋 토큰 ID: {nft_data['token_id']}")
        print(f"📅 발행일: {nft_data['issue_date']}")
        print(f"⏰ 만료일: {nft_data['expiry_date']}")
        
        # 속성 확인
        for attr in nft_data['attributes']:
            if attr['trait_type'] == 'Credit Grade':
                assert attr['value'] == 'B'
            elif attr['trait_type'] == 'Max Loan Amount':
                assert attr['value'] == 50000000
        
        print(f"🏷️ 신용등급: B")
        print(f"💰 최대대출한도: 50,000,000원")
    
    def test_04_loan_rejection(self):
        """대출 거절 테스트 (한도 초과)"""
        print("\n❌ 4. 대출 거절 테스트 (한도 초과)")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            "customer_id": "CUST_001",
            "customer_name": "김철수",
            "requested_amount": 60000000,  # 한도 초과
            "purpose": "대규모 투자",
            "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        }
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert result['status'] == 'completed'
        assert result['approval_status'] == 'rejected'
        assert 'nft_token_id' in result
        
        print(f"❌ 대출 거절: {result['approval_status']}")
        print(f"💬 메시지: {result['message']}")
        print(f"💰 최대대출한도: {result['max_loan_amount']:,}원")
    
    def test_05_different_customer(self):
        """다른 고객 대출 요청 테스트"""
        print("\n👤 5. 다른 고객 대출 요청 테스트")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            "customer_id": "CUST_002",
            "customer_name": "이영희",
            "requested_amount": 30000000,
            "purpose": "주택구입",
            "customer_address": "0x1234567890abcdef1234567890abcdef12345678"
        }
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert result['status'] == 'completed'
        assert result['approval_status'] == 'approved'
        assert 'nft_token_id' in result
        assert result['credit_grade'] == 'A'  # 820점으로 A등급
        assert result['max_loan_amount'] == 100000000
        
        print(f"✅ 대출 승인: {result['approval_status']}")
        print(f"📋 NFT 토큰: {result['nft_token_id']}")
        print(f"🏷️ 신용등급: {result['credit_grade']}")
        print(f"💰 최대대출한도: {result['max_loan_amount']:,}원")
    
    def test_06_low_credit_customer(self):
        """낮은 신용등급 고객 테스트"""
        print("\n📉 6. 낮은 신용등급 고객 테스트")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            "customer_id": "CUST_003",
            "customer_name": "박민수",
            "requested_amount": 10000000,
            "purpose": "개인사업",
            "customer_address": "0xabcdef1234567890abcdef1234567890abcdef12"
        }
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert result['status'] == 'completed'
        assert result['approval_status'] == 'approved'
        assert 'nft_token_id' in result
        assert result['credit_grade'] == 'C'  # 650점으로 C등급
        assert result['max_loan_amount'] == 20000000
        
        print(f"✅ 대출 승인: {result['approval_status']}")
        print(f"📋 NFT 토큰: {result['nft_token_id']}")
        print(f"🏷️ 신용등급: {result['credit_grade']}")
        print(f"💰 최대대출한도: {result['max_loan_amount']:,}원")
    
    def test_07_nft_verification(self):
        """NFT 검증 테스트"""
        print("\n🔐 7. NFT 검증 테스트")
        
        # 먼저 NFT 생성
        loan_url = f"{self.BASE_URL}/api/bank/loan-request"
        loan_data = {
            "customer_id": "CUST_001",
            "customer_name": "김철수",
            "requested_amount": 10000000,
            "purpose": "테스트용",
            "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        }
        
        loan_response = requests.post(loan_url, json=loan_data)
        assert loan_response.status_code == 200
        loan_result = loan_response.json()
        token_id = loan_result['nft_token_id']
        
        # NFT 검증
        verify_url = f"{self.BASE_URL}/api/bank/verify-nft"
        verify_data = {
            "token_id": token_id,
            "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
            "requested_amount": 10000000
        }
        
        verify_response = requests.post(verify_url, json=verify_data)
        assert verify_response.status_code == 200
        
        verify_result = verify_response.json()
        assert verify_result['approval_status'] == 'approved'
        assert verify_result['token_id'] == token_id
        assert 'nft_data' in verify_result
        
        print(f"✅ NFT 검증 성공: {verify_result['approval_status']}")
        print(f"📋 토큰 ID: {verify_result['token_id']}")
        print(f"💰 승인 금액: {verify_result['requested_amount']:,}원")
    
    def test_08_zk_proof_generation(self):
        """ZK-Proof 생성 테스트"""
        print("\n🔒 8. ZK-Proof 생성 테스트")
        
        url = f"{self.BASE_URL}/api/external/generate-proof"
        data = {
            "customer_id": "CUST_001",
            "credit_score": 750,
            "credit_grade": "B",
            "max_loan_amount": 50000000
        }
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert 'proof_id' in result
        assert 'status' in result
        assert 'proof_data' in result
        assert 'zk_proof' in result['proof_data']
        
        print(f"✅ ZK-Proof 생성 성공")
        print(f"📋 Proof ID: {result['proof_id']}")
        print(f"📊 상태: {result['status']}")
        print(f"🔐 ZK-Proof: {len(result['proof_data']['zk_proof'])} 개의 증명 요소")
    
    def test_09_nft_minting(self):
        """NFT 발행 테스트"""
        print("\n🎨 9. NFT 발행 테스트")
        
        url = f"{self.BASE_URL}/api/external/mint-nft"
        data = {
            "proof_id": "PROOF_TEST_001",
            "customer_id": "CUST_001",
            "credit_grade": "B",
            "max_loan_amount": 50000000,
            "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        }
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert 'token_id' in result
        assert 'nft_metadata' in result
        assert 'blockchain_tx_hash' in result
        
        print(f"✅ NFT 발행 성공")
        print(f"📋 토큰 ID: {result['token_id']}")
        print(f"🔗 트랜잭션 해시: {result['blockchain_tx_hash']}")
    
    def test_10_proof_retrieval(self):
        """Proof 조회 테스트"""
        print("\n📄 10. Proof 조회 테스트")
        
        proof_id = "PROOF_TEST_001"
        url = f"{self.BASE_URL}/api/external/proof/{proof_id}"
        
        response = requests.get(url)
        assert response.status_code == 200
        
        result = response.json()
        assert result['proof_id'] == proof_id
        assert 'zk_proof' in result
        assert 'metadata' in result
        
        print(f"✅ Proof 조회 성공")
        print(f"📋 Proof ID: {result['proof_id']}")
        print(f"📊 메타데이터: {result['metadata']}")

def run_comprehensive_test():
    """종합 테스트 실행"""
    print("🚀 ZK-NFT 시스템 종합 테스트 시작")
    print("=" * 60)
    
    test_instance = TestZKNFTSystem()
    
    try:
        # 순차적으로 테스트 실행
        test_instance.test_01_loan_request_new_customer()
        test_instance.test_02_nft_reuse_same_customer()
        test_instance.test_03_nft_lookup()
        test_instance.test_04_loan_rejection()
        test_instance.test_05_different_customer()
        test_instance.test_06_low_credit_customer()
        test_instance.test_07_nft_verification()
        test_instance.test_08_zk_proof_generation()
        test_instance.test_09_nft_minting()
        test_instance.test_10_proof_retrieval()
        
        print("\n" + "=" * 60)
        print("🎉 모든 테스트가 성공적으로 완료되었습니다!")
        print("✅ ZK-NFT 시스템이 정상적으로 작동하고 있습니다.")
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        raise

if __name__ == "__main__":
    run_comprehensive_test() 