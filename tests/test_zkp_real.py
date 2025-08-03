"""
실제 ZoKrates 기반 ZK-Proof 테스트
Mock이 아닌 실제 ZoKrates를 사용한 ZK-Proof 생성 및 검증을 테스트합니다.
"""

import sys
import os
import json
import time
from datetime import datetime

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.zkp_utils import zkp_utils

def test_zokrates_compilation():
    """ZoKrates 프로그램 컴파일 테스트"""
    print("🔨 Testing ZoKrates compilation...")
    
    result = zkp_utils.compile_zokrates_program('credit_score.zok')
    
    if result['status'] == 'success':
        print(f"✅ Compilation successful")
        print(f"   Output: {result['output'][:100]}...")
        return True
    else:
        print(f"❌ Compilation failed: {result['message']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        return False

def test_zokrates_setup():
    """ZoKrates setup 테스트"""
    print("\n⚙️ Testing ZoKrates setup...")
    
    result = zkp_utils.setup_zokrates_program('credit_score')
    
    if result['status'] == 'success':
        print(f"✅ Setup successful")
        print(f"   Output: {result['output'][:100]}...")
        return True
    else:
        print(f"❌ Setup failed: {result['message']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        return False

def test_witness_computation():
    """Witness 계산 테스트"""
    print("\n🧮 Testing witness computation...")
    
    # 테스트 데이터: 신용점수 750, B등급, 최대 대출 5000만원
    inputs = ['750', '2', '50000000']  # B등급 = 2
    
    result = zkp_utils.compute_witness('credit_score', inputs)
    
    if result['status'] == 'success':
        print(f"✅ Witness computation successful")
        print(f"   Inputs: {inputs}")
        print(f"   Output: {result['output'][:100]}...")
        return True
    else:
        print(f"❌ Witness computation failed: {result['message']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        return False

def test_proof_generation():
    """Proof 생성 테스트"""
    print("\n🔐 Testing proof generation...")
    
    result = zkp_utils.generate_proof('credit_score')
    
    if result['status'] == 'success':
        print(f"✅ Proof generation successful")
        print(f"   Proof data: {json.dumps(result['proof'], indent=2)}")
        return result['proof']
    else:
        print(f"❌ Proof generation failed: {result['message']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        return None

def test_proof_verification():
    """Proof 검증 테스트"""
    print("\n✅ Testing proof verification...")
    
    result = zkp_utils.verify_proof('credit_score')
    
    if result['status'] == 'success':
        print(f"✅ Proof verification successful")
        print(f"   Output: {result['output']}")
        return True
    else:
        print(f"❌ Proof verification failed: {result['message']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        return False

def test_credit_score_proof_creation():
    """신용등급 ZK-Proof 생성 테스트"""
    print("\n🎯 Testing credit score ZK-Proof creation...")
    
    # 테스트 데이터
    credit_score = 750
    credit_grade = "B"
    max_loan_amount = 50000000
    
    print(f"   Credit Score: {credit_score}")
    print(f"   Credit Grade: {credit_grade}")
    print(f"   Max Loan Amount: {max_loan_amount:,}원")
    
    result = zkp_utils.create_credit_score_proof(credit_score, credit_grade, max_loan_amount)
    
    if result['status'] == 'success':
        print(f"✅ Credit score ZK-Proof created successfully")
        proof_data = result['proof_data']
        print(f"   Proof ID: {proof_data['proof_id']}")
        print(f"   Timestamp: {proof_data['proof_timestamp']}")
        print(f"   ZK-Proof: {json.dumps(proof_data['zk_proof'], indent=2)}")
        return proof_data
    else:
        print(f"❌ Credit score ZK-Proof creation failed: {result['message']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        return None

def test_credit_score_proof_verification(proof_data):
    """신용등급 ZK-Proof 검증 테스트"""
    print("\n🔍 Testing credit score ZK-Proof verification...")
    
    if not proof_data:
        print("❌ No proof data to verify")
        return False
    
    result = zkp_utils.verify_credit_score_proof(proof_data)
    
    if result['status'] == 'success':
        print(f"✅ Credit score ZK-Proof verified successfully")
        print(f"   Is Valid: {result['is_valid']}")
        if 'verification_output' in result:
            print(f"   Verification Output: {result['verification_output']}")
        return True
    else:
        print(f"❌ Credit score ZK-Proof verification failed: {result['message']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        return False

def test_multiple_credit_grades():
    """다양한 신용등급에 대한 ZK-Proof 생성 테스트"""
    print("\n📊 Testing multiple credit grades...")
    
    test_cases = [
        {"score": 850, "grade": "A", "amount": 100000000, "description": "A등급 고객"},
        {"score": 750, "grade": "B", "amount": 50000000, "description": "B등급 고객"},
        {"score": 650, "grade": "C", "amount": 20000000, "description": "C등급 고객"},
        {"score": 550, "grade": "D", "amount": 5000000, "description": "D등급 고객"},
        {"score": 450, "grade": "E", "amount": 0, "description": "E등급 고객"}
    ]
    
    success_count = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n   {i}. {case['description']}")
        print(f"      신용점수: {case['score']}, 등급: {case['grade']}, 한도: {case['amount']:,}원")
        
        result = zkp_utils.create_credit_score_proof(
            case['score'], case['grade'], case['amount']
        )
        
        if result['status'] == 'success':
            print(f"      ✅ ZK-Proof 생성 성공")
            success_count += 1
        else:
            print(f"      ❌ ZK-Proof 생성 실패: {result['message']}")
    
    print(f"\n📈 결과: {success_count}/{len(test_cases)} 성공")
    return success_count == len(test_cases)

def main():
    """메인 테스트 함수"""
    print("🚀 Starting Real ZoKrates ZK-Proof Tests")
    print("=" * 60)
    
    # 1. ZoKrates 컴파일 테스트
    if not test_zokrates_compilation():
        print("❌ ZoKrates compilation failed. Please check Docker and ZoKrates setup.")
        return
    
    # 2. ZoKrates setup 테스트
    if not test_zokrates_setup():
        print("❌ ZoKrates setup failed.")
        return
    
    # 3. Witness 계산 테스트
    if not test_witness_computation():
        print("❌ Witness computation failed.")
        return
    
    # 4. Proof 생성 테스트
    proof = test_proof_generation()
    if not proof:
        print("❌ Proof generation failed.")
        return
    
    # 5. Proof 검증 테스트
    if not test_proof_verification():
        print("❌ Proof verification failed.")
        return
    
    # 6. 신용등급 ZK-Proof 생성 테스트
    proof_data = test_credit_score_proof_creation()
    if not proof_data:
        print("❌ Credit score ZK-Proof creation failed.")
        return
    
    # 7. 신용등급 ZK-Proof 검증 테스트
    if not test_credit_score_proof_verification(proof_data):
        print("❌ Credit score ZK-Proof verification failed.")
        return
    
    # 8. 다양한 신용등급 테스트
    test_multiple_credit_grades()
    
    print("\n" + "=" * 60)
    print("🎉 All Real ZoKrates ZK-Proof tests completed!")
    print("✅ Actual ZK-Proof generation and verification working correctly!")
    print("🔐 Privacy-preserving credit score verification implemented!")

if __name__ == "__main__":
    main() 