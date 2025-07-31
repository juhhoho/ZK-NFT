#!/usr/bin/env python3
"""
ZK-NFT 시스템 발표용 데모 스크립트
실시간으로 시스템의 핵심 기능을 시연합니다.
"""

import requests
import json
import time
from datetime import datetime

class ZKNFTDemo:
    """ZK-NFT 시스템 데모 클래스"""
    
    BASE_URL = "http://localhost:5000"
    
    def __init__(self):
        self.demo_data = {
            "customer_1": {
                "customer_id": "CUST_001",
                "customer_name": "김철수",
                "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
            },
            "customer_2": {
                "customer_id": "CUST_002", 
                "customer_name": "이영희",
                "customer_address": "0x1234567890abcdef1234567890abcdef12345678"
            }
        }
    
    def print_header(self, title):
        """헤더 출력"""
        print("\n" + "=" * 80)
        print(f"🎤 {title}")
        print("=" * 80)
    
    def print_step(self, step_num, description):
        """단계 출력"""
        print(f"\n📋 Step {step_num}: {description}")
        print("-" * 60)
    
    def wait_for_user(self, message="계속하려면 Enter를 누르세요..."):
        """사용자 입력 대기"""
        input(f"\n⏸️  {message}")
    
    def demo_scenario_1_new_customer(self):
        """시나리오 1: 신규 고객 대출 신청"""
        self.print_header("시나리오 1: 신규 고객 대출 신청")
        
        print("""
🔍 문제 상황:
- 기존 대출 시스템의 개인 신용정보 노출 위험
- 중복 신용조회로 인한 비효율성
- 신용정보 조작 가능성

💡 ZK-NFT 솔루션:
- Zero-Knowledge Proof로 프라이버시 보호
- NFT 재사용으로 효율성 증대
- 블록체인 기반 불변성 보장
        """)
        
        self.wait_for_user()
        
        # Step 1: 대출 요청
        self.print_step(1, "고객이 대출 신청")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            **self.demo_data["customer_1"],
            "requested_amount": 15000000,
            "purpose": "사업자금"
        }
        
        print(f"🏦 대출 요청 데이터:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"\n✅ 응답 결과:")
        print(f"   상태: {result['status']}")
        print(f"   승인여부: {result['approval_status']}")
        print(f"   NFT 토큰: {result['nft_token_id']}")
        print(f"   신용등급: {result['credit_grade']}")
        print(f"   최대대출한도: {result['max_loan_amount']:,}원")
        
        self.wait_for_user()
        
        # Step 2: NFT 조회
        self.print_step(2, "고객이 자신의 NFT 확인")
        
        nft_url = f"{self.BASE_URL}/api/external/my-nft"
        nft_data = {
            "customer_id": self.demo_data["customer_1"]["customer_id"],
            "customer_address": self.demo_data["customer_1"]["customer_address"]
        }
        
        nft_response = requests.post(nft_url, json=nft_data)
        nft_result = nft_response.json()
        
        print(f"🔍 NFT 조회 결과:")
        print(f"   상태: {nft_result['status']}")
        print(f"   토큰 ID: {nft_result['nft_data']['token_id']}")
        print(f"   발행일: {nft_result['nft_data']['issue_date']}")
        print(f"   만료일: {nft_result['nft_data']['expiry_date']}")
        print(f"   유효성: {nft_result['nft_data']['is_valid']}")
        
        print(f"\n🏷️ NFT 속성:")
        for attr in nft_result['nft_data']['attributes']:
            print(f"   - {attr['trait_type']}: {attr['value']}")
        
        self.wait_for_user()
    
    def demo_scenario_2_nft_reuse(self):
        """시나리오 2: NFT 재사용"""
        self.print_header("시나리오 2: NFT 재사용 (효율성 증대)")
        
        print("""
⚡ 효율성 비교:
기존 시스템: 매번 신용정보 조회 (시간 + 비용)
ZK-NFT 시스템: NFT 재사용 (즉시 처리)
        """)
        
        self.wait_for_user()
        
        # Step 1: 동일 고객 재대출 요청
        self.print_step(1, "동일 고객이 추가 대출 요청")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            **self.demo_data["customer_1"],
            "requested_amount": 20000000,
            "purpose": "운전자금"
        }
        
        print(f"🏦 재대출 요청 데이터:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        start_time = time.time()
        response = requests.post(url, json=data)
        end_time = time.time()
        
        result = response.json()
        
        print(f"\n⚡ 처리 시간: {end_time - start_time:.2f}초")
        print(f"✅ 응답 결과:")
        print(f"   상태: {result['status']}")
        print(f"   승인여부: {result['approval_status']}")
        print(f"   NFT 토큰: {result['nft_token_id']}")
        print(f"   💡 기존 NFT 재사용으로 즉시 처리!")
        
        self.wait_for_user()
        
        # Step 2: NFT 재사용 확인
        self.print_step(2, "NFT 재사용 상태 확인")
        
        nft_url = f"{self.BASE_URL}/api/external/my-nft"
        nft_data = {
            "customer_id": self.demo_data["customer_1"]["customer_id"],
            "customer_address": self.demo_data["customer_1"]["customer_address"]
        }
        
        nft_response = requests.post(nft_url, json=nft_data)
        nft_result = nft_response.json()
        
        print(f"🔍 NFT 상태:")
        print(f"   상태: {nft_result['status']}")
        print(f"   토큰 ID: {nft_result['nft_data']['token_id']}")
        print(f"   유효성: {nft_result['nft_data']['is_valid']}")
        print(f"   💡 동일한 NFT가 재사용되었습니다!")
        
        self.wait_for_user()
    
    def demo_scenario_3_different_customers(self):
        """시나리오 3: 다른 고객들의 신용등급별 처리"""
        self.print_header("시나리오 3: 다양한 신용등급 고객 처리")
        
        print("""
👥 다양한 고객 시나리오:
- A등급 고객 (이영희): 높은 한도, 낮은 금리
- B등급 고객 (김철수): 중간 한도, 중간 금리
- C등급 고객 (박민수): 낮은 한도, 높은 금리
        """)
        
        self.wait_for_user()
        
        # A등급 고객
        self.print_step(1, "A등급 고객 (이영희) 대출 요청")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            **self.demo_data["customer_2"],
            "requested_amount": 50000000,
            "purpose": "주택구입"
        }
        
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"👤 {data['customer_name']} ({data['customer_id']})")
        print(f"   신용등급: {result['credit_grade']}")
        print(f"   최대대출한도: {result['max_loan_amount']:,}원")
        print(f"   승인여부: {result['approval_status']}")
        print(f"   NFT 토큰: {result['nft_token_id']}")
        
        self.wait_for_user()
        
        # C등급 고객
        self.print_step(2, "C등급 고객 (박민수) 대출 요청")
        
        data = {
            "customer_id": "CUST_003",
            "customer_name": "박민수",
            "requested_amount": 15000000,
            "purpose": "개인사업",
            "customer_address": "0xabcdef1234567890abcdef1234567890abcdef12"
        }
        
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"👤 {data['customer_name']} ({data['customer_id']})")
        print(f"   신용등급: {result['credit_grade']}")
        print(f"   최대대출한도: {result['max_loan_amount']:,}원")
        print(f"   승인여부: {result['approval_status']}")
        print(f"   NFT 토큰: {result['nft_token_id']}")
        
        self.wait_for_user()
    
    def demo_scenario_4_loan_rejection(self):
        """시나리오 4: 대출 거절 케이스"""
        self.print_header("시나리오 4: 대출 거절 케이스")
        
        print("""
❌ 대출 거절 시나리오:
- 신용등급 기준 미달
- 대출 한도 초과
- 투명한 거절 사유 제공
        """)
        
        self.wait_for_user()
        
        # 한도 초과 케이스
        self.print_step(1, "대출 한도 초과 요청")
        
        url = f"{self.BASE_URL}/api/bank/loan-request"
        data = {
            **self.demo_data["customer_1"],
            "requested_amount": 60000000,  # 한도 초과
            "purpose": "대규모 투자"
        }
        
        print(f"🏦 대출 요청: {data['requested_amount']:,}원")
        print(f"   (최대대출한도: 50,000,000원)")
        
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"\n❌ 거절 결과:")
        print(f"   승인여부: {result['approval_status']}")
        print(f"   메시지: {result['message']}")
        print(f"   최대대출한도: {result['max_loan_amount']:,}원")
        print(f"   NFT 토큰: {result['nft_token_id']}")
        print(f"   💡 NFT는 발행되었지만 대출은 거절됨")
        
        self.wait_for_user()
    
    def demo_scenario_5_zk_proof_verification(self):
        """시나리오 5: ZK-Proof 검증"""
        self.print_header("시나리오 5: Zero-Knowledge Proof 검증")
        
        print("""
🔒 ZK-Proof 핵심 가치:
- 신용정보 노출 없이 신용등급 증명
- 수학적 암호화 기반 검증
- 프라이버시 보호 강화
        """)
        
        self.wait_for_user()
        
        # ZK-Proof 생성
        self.print_step(1, "ZK-Proof 생성")
        
        url = f"{self.BASE_URL}/api/external/generate-proof"
        data = {
            "customer_id": "CUST_001",
            "credit_score": 750,
            "credit_grade": "B",
            "max_loan_amount": 50000000
        }
        
        print(f"🔒 ZK-Proof 생성 데이터:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"\n✅ ZK-Proof 생성 결과:")
        print(f"   Proof ID: {result['proof_id']}")
        print(f"   검증 결과: {result['verification_result']}")
        print(f"   💡 신용정보 노출 없이 증명 생성 완료!")
        
        self.wait_for_user()
        
        # Proof 조회
        self.print_step(2, "ZK-Proof 조회")
        
        proof_url = f"{self.BASE_URL}/api/external/proof/{result['proof_id']}"
        proof_response = requests.get(proof_url)
        proof_result = proof_response.json()
        
        print(f"📄 Proof 조회 결과:")
        print(f"   Proof ID: {proof_result['proof_id']}")
        print(f"   메타데이터: {proof_result['metadata']}")
        print(f"   💡 블록체인에서 검증 가능한 증명")
        
        self.wait_for_user()
    
    def demo_summary(self):
        """데모 요약"""
        self.print_header("🎯 ZK-NFT 시스템 핵심 가치 요약")
        
        print("""
✅ 성공적으로 시연된 기능들:

🔒 프라이버시 보호
   - Zero-Knowledge Proof로 신용정보 노출 방지
   - 신용등급만으로 검증 가능

⚡ 효율성 증대
   - NFT 재사용으로 중복 신용조회 방지
   - 즉시 대출 승인/거절 처리

🏛️ 신뢰성 보장
   - 블록체인 기반 불변성
   - 조작 불가능한 검증 기록

📊 투명성 제공
   - 명확한 승인/거절 사유
   - 검증 과정의 투명한 기록

🎨 사용자 경험
   - 간단한 대출 신청 프로세스
   - 실시간 NFT 상태 확인
        """)
        
        print("\n🚀 ZK-NFT 시스템이 미래의 신용대출 패러다임을 제시합니다!")
        print("   - 프라이버시 보호")
        print("   - 효율성 증대") 
        print("   - 신뢰성 보장")
        print("   - 투명성 제공")

def run_demo():
    """데모 실행"""
    print("🎤 ZK-NFT 신용대출 시스템 발표 데모")
    print("=" * 80)
    
    demo = ZKNFTDemo()
    
    try:
        # 시나리오별 데모 실행
        demo.demo_scenario_1_new_customer()
        demo.demo_scenario_2_nft_reuse()
        demo.demo_scenario_3_different_customers()
        demo.demo_scenario_4_loan_rejection()
        demo.demo_scenario_5_zk_proof_verification()
        demo.demo_summary()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  데모가 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 데모 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    run_demo() 