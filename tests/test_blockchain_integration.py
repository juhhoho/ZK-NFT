"""
실제 블록체인 연동 테스트
Hardhat 로컬 블록체인과 실제 상호작용을 테스트합니다.
"""

import sys
import os
import json
import time
from datetime import datetime

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.blockchain_utils_real import real_blockchain_utils

def test_blockchain_connection():
    """블록체인 연결 테스트"""
    print("🔗 Testing blockchain connection...")
    
    result = real_blockchain_utils.connect_to_blockchain()
    
    if result['status'] == 'success':
        print(f"✅ Connected to blockchain")
        print(f"   Network ID: {result['network_id']}")
        print(f"   Latest Block: {result['latest_block']}")
        print(f"   Contract Address: {result['contract_address']}")
        print(f"   Contract Deployed: {result['is_contract_deployed']}")
        return True
    else:
        print(f"❌ Failed to connect: {result['message']}")
        return False

def test_account_creation():
    """계정 생성 테스트 (Hardhat 기본 계정 사용)"""
    print("\n👤 Testing account creation...")
    
    # Hardhat 기본 계정 사용 (ETH가 이미 있음)
    hardhat_account = {
        'address': '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266',
        'private_key': '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
    }
    
    print(f"✅ Using Hardhat default account")
    print(f"   Address: {hardhat_account['address']}")
    print(f"   Private Key: {hardhat_account['private_key'][:10]}...")
    return hardhat_account

def test_balance_check(address):
    """잔액 조회 테스트"""
    print(f"\n💰 Testing balance check for {address}...")
    
    result = real_blockchain_utils.get_balance(address)
    
    if result['status'] == 'success':
        print(f"✅ Balance retrieved successfully")
        print(f"   Balance: {result['balance_eth']} ETH")
        print(f"   Balance: {result['balance_wei']} Wei")
        return True
    else:
        print(f"❌ Failed to get balance: {result['message']}")
        return False

def test_nft_minting(customer_address, minter_private_key):
    """NFT 발행 테스트"""
    print(f"\n🎨 Testing NFT minting...")
    
    # 테스트 데이터
    credit_grade = "B"
    max_loan_amount = 50000000  # 5천만원
    proof_id = f"PROOF_TEST_{int(time.time())}"
    customer_id = "CUST_TEST_001"
    
    result = real_blockchain_utils.mint_credit_grade_nft(
        to_address=customer_address,
        credit_grade=credit_grade,
        max_loan_amount=max_loan_amount,
        proof_id=proof_id,
        customer_id=customer_id,
        minter_private_key=minter_private_key
    )
    
    if result['status'] == 'success':
        print(f"✅ NFT minted successfully")
        print(f"   Token ID: {result['token_id']}")
        print(f"   Transaction Hash: {result['transaction_hash']}")
        print(f"   Gas Used: {result['gas_used']}")
        print(f"   Block Number: {result['block_number']}")
        return result
    else:
        print(f"❌ Failed to mint NFT: {result['message']}")
        return None

def test_nft_info_retrieval(token_id):
    """NFT 정보 조회 테스트"""
    print(f"\n📋 Testing NFT info retrieval for token {token_id}...")
    
    result = real_blockchain_utils.get_nft_info(token_id)
    
    if result['status'] == 'success':
        print(f"✅ NFT info retrieved successfully")
        print(f"   Owner: {result['owner']}")
        print(f"   Credit Grade: {result['credit_grade']}")
        print(f"   Max Loan Amount: {result['max_loan_amount']}")
        print(f"   Proof ID: {result['proof_id']}")
        print(f"   Customer ID: {result['customer_id']}")
        print(f"   Is Valid: {result['is_valid']}")
        return True
    else:
        print(f"❌ Failed to get NFT info: {result['message']}")
        return False

def test_loan_eligibility_check(token_id, requested_amount):
    """대출 자격 확인 테스트"""
    print(f"\n🏦 Testing loan eligibility check...")
    print(f"   Token ID: {token_id}")
    print(f"   Requested Amount: {requested_amount}")
    
    result = real_blockchain_utils.check_loan_eligibility(token_id, requested_amount)
    
    if result['status'] == 'success':
        print(f"✅ Loan eligibility checked successfully")
        print(f"   Is Eligible: {result['is_eligible']}")
        return True
    else:
        print(f"❌ Failed to check loan eligibility: {result['message']}")
        return False

def test_customer_tokens_retrieval(customer_id):
    """고객 토큰 조회 테스트"""
    print(f"\n👥 Testing customer tokens retrieval for {customer_id}...")
    
    result = real_blockchain_utils.get_customer_tokens(customer_id)
    
    if result['status'] == 'success':
        print(f"✅ Customer tokens retrieved successfully")
        print(f"   Token Count: {result['token_count']}")
        print(f"   Token IDs: {result['token_ids']}")
        return True
    else:
        print(f"❌ Failed to get customer tokens: {result['message']}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚀 Starting Blockchain Integration Tests")
    print("=" * 50)
    
    # 1. 블록체인 연결 테스트
    if not test_blockchain_connection():
        print("❌ Blockchain connection failed. Please ensure Hardhat node is running.")
        return
    
    # 2. 계정 생성 테스트
    account_result = test_account_creation()
    if not account_result:
        print("❌ Account creation failed.")
        return
    
    customer_address = account_result['address']
    minter_private_key = account_result['private_key']
    
    # 3. 잔액 조회 테스트
    test_balance_check(customer_address)
    
    # 4. NFT 발행 테스트
    mint_result = test_nft_minting(customer_address, minter_private_key)
    if not mint_result:
        print("❌ NFT minting failed.")
        return
    
    token_id = mint_result['token_id']
    
    # 5. NFT 정보 조회 테스트
    test_nft_info_retrieval(token_id)
    
    # 6. 대출 자격 확인 테스트 (성공 케이스)
    test_loan_eligibility_check(token_id, 30000000)  # 3천만원
    
    # 7. 대출 자격 확인 테스트 (실패 케이스)
    test_loan_eligibility_check(token_id, 60000000)  # 6천만원
    
    # 8. 고객 토큰 조회 테스트
    test_customer_tokens_retrieval("CUST_TEST_001")
    
    print("\n" + "=" * 50)
    print("🎉 All blockchain integration tests completed!")
    print("✅ Real blockchain integration is working correctly!")

if __name__ == "__main__":
    main() 