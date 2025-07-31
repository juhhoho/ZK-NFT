"""
외부기관 관련 API 엔드포인트
신용정보 조회, ZK-Proof 생성, NFT 발행 등의 기능을 제공합니다.
"""

from flask import Blueprint, request, jsonify
import json
import os
import hashlib
from datetime import datetime
import subprocess
import tempfile

external_bp = Blueprint('external', __name__)

# Mock 신용정보 데이터 로드
def load_credit_data():
    """Mock 신용정보 데이터를 로드합니다."""
    try:
        with open('data/credit_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 기본 Mock 데이터 반환
        return {
            "customers": {
                "CUST_001": {
                    "name": "김철수",
                    "credit_score": 750,
                    "income": 50000000,
                    "debt_ratio": 0.3,
                    "payment_history": "excellent",
                    "employment_status": "full_time",
                    "residence_stability": 5
                },
                "CUST_002": {
                    "name": "이영희",
                    "credit_score": 820,
                    "income": 70000000,
                    "debt_ratio": 0.2,
                    "payment_history": "excellent",
                    "employment_status": "full_time",
                    "residence_stability": 8
                },
                "CUST_003": {
                    "name": "박민수",
                    "credit_score": 650,
                    "income": 35000000,
                    "debt_ratio": 0.5,
                    "payment_history": "good",
                    "employment_status": "full_time",
                    "residence_stability": 3
                }
            }
        }

def calculate_credit_grade(credit_score):
    """신용점수를 기반으로 신용등급을 계산합니다."""
    if credit_score >= 800:
        return "A"
    elif credit_score >= 700:
        return "B"
    elif credit_score >= 600:
        return "C"
    elif credit_score >= 500:
        return "D"
    else:
        return "E"

# Mock NFT 저장소 (실제로는 데이터베이스 사용)
nft_storage = {}

def get_existing_nft(customer_id, customer_address):
    """고객의 기존 NFT를 조회합니다."""
    key = f"{customer_id}_{customer_address}"
    return nft_storage.get(key)

def is_nft_valid(nft_data):
    """NFT의 유효기간을 확인합니다."""
    try:
        expiry_date = datetime.fromisoformat(nft_data['expiry_date'].replace('Z', '+00:00'))
        current_time = datetime.now(expiry_date.tzinfo)
        return current_time < expiry_date
    except:
        return False

def save_nft(customer_id, customer_address, nft_data):
    """NFT를 저장합니다."""
    key = f"{customer_id}_{customer_address}"
    nft_storage[key] = nft_data

@external_bp.route('/credit-inquiry', methods=['POST'])
def credit_inquiry():
    """
    고객의 신용정보를 조회하고 ZK-Proof를 생성하여 NFT를 발행합니다.
    
    Request Body:
    {
        "customer_id": "고객 ID",
        "customer_name": "고객명",
        "requested_amount": 10000000,
        "purpose": "대출 목적",
        "request_timestamp": "2024-01-15T10:00:00Z",
        "bank_id": "BANK_001",
        "customer_address": "0x..." (NFT 발행용)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['customer_id', 'customer_name', 'requested_amount', 'purpose', 'request_id', 'customer_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        customer_id = data['customer_id']
        customer_name = data['customer_name']
        requested_amount = data['requested_amount']
        request_id = data['request_id']
        customer_address = data['customer_address']
        
        print(f"🏛️ [EXTERNAL] 신용정보 조회 요청 접수: {customer_name}({customer_id})")
        print(f"🏛️ [EXTERNAL] Request ID: {request_id}")
        print(f"🏛️ [EXTERNAL] 요청 금액: {requested_amount:,}원")
        
        # 기존 NFT 확인 (만료 체크)
        existing_nft = get_existing_nft(customer_id, customer_address)
        
        if existing_nft and is_nft_valid(existing_nft):
            # 기존 NFT가 유효하면 재사용
            print(f"🏛️ [EXTERNAL] 기존 NFT 발견: {existing_nft['token_id']}")
            print(f"🏛️ [EXTERNAL] NFT 유효기간 확인: 유효함")
            
            # NFT에서 신용정보 추출
            credit_grade = None
            max_loan_amount = None
            
            for attr in existing_nft['attributes']:
                if attr['trait_type'] == 'Credit Grade':
                    credit_grade = attr['value']
                elif attr['trait_type'] == 'Max Loan Amount':
                    max_loan_amount = attr['value']
            
            print(f"🏛️ [EXTERNAL] NFT에서 신용정보 추출: {credit_grade}등급, {max_loan_amount:,}원")
            
            # 기존 NFT 재사용
            token_id = existing_nft['token_id']
            nft_metadata = existing_nft
            proof_data = {
                'proof_id': existing_nft['proof_id'],
                'zk_proof': {
                    'a': ['0x1234567890abcdef', '0xabcdef1234567890'],
                    'b': [['0x1111111111111111', '0x2222222222222222'], ['0x3333333333333333', '0x4444444444444444']],
                    'c': ['0x5555555555555555', '0x6666666666666666']
                }
            }
            inquiry_id = f'INQ_{customer_id}_{int(datetime.now().timestamp())}'
            
        else:
            # 새로운 신용정보 조회 및 NFT 생성
            print(f"🏛️ [EXTERNAL] 기존 NFT 없음 또는 만료됨 - 새로운 신용정보 조회 시작")
            
            # Mock 신용정보 데이터에서 고객 정보 조회
            credit_data = load_credit_data()
            
            if customer_id not in credit_data['customers']:
                return jsonify({'error': 'Customer not found'}), 404
            
            customer_info = credit_data['customers'][customer_id]
            credit_grade = calculate_credit_grade(customer_info['credit_score'])
            
            print(f"🏛️ [EXTERNAL] 신용정보 조회 완료: {customer_info['credit_score']}점 → {credit_grade}등급")
            
            # 신용등급별 대출 한도 설정
            loan_limits = {
                "A": 100000000,  # 1억원
                "B": 50000000,   # 5천만원
                "C": 20000000,   # 2천만원
                "D": 5000000,    # 5백만원
                "E": 0
            }
            
            max_loan_amount = loan_limits.get(credit_grade, 0)
            print(f"🏛️ [EXTERNAL] 대출 한도 계산: {max_loan_amount:,}원")
        
        # ZK-Proof 생성 (기존 NFT가 없거나 만료된 경우에만)
        if not (existing_nft and is_nft_valid(existing_nft)):
            inquiry_id = f'INQ_{customer_id}_{int(datetime.now().timestamp())}'
            proof_data = {
                'proof_id': f'PROOF_{inquiry_id}',
                'customer_id': customer_id,
                'credit_score_hash': hashlib.sha256(str(customer_info['credit_score']).encode()).hexdigest(),
                'credit_grade_hash': hashlib.sha256(credit_grade.encode()).hexdigest(),
                'max_loan_amount_hash': hashlib.sha256(str(max_loan_amount).encode()).hexdigest(),
                'proof_timestamp': datetime.now().isoformat(),
                'zk_proof': {
                    'a': ['0x1234567890abcdef', '0xabcdef1234567890'],
                    'b': [['0x1111111111111111', '0x2222222222222222'], ['0x3333333333333333', '0x4444444444444444']],
                    'c': ['0x5555555555555555', '0x6666666666666666']
                }
            }
            print(f"🏛️ [EXTERNAL] ZK-Proof 생성 완료: {proof_data['proof_id']}")
            print(f"🏛️ [EXTERNAL] Inquiry ID: {inquiry_id}")
            
            # 새로운 NFT 발행
            current_time = datetime.now()
            issue_date = current_time.isoformat()
            expiry_date = (current_time.replace(day=current_time.day + 30)).isoformat()  # 1개월 후
            
            token_id = f'NFT_{proof_data["proof_id"]}_{int(current_time.timestamp())}'
            print(f"🏛️ [EXTERNAL] 새로운 NFT 생성: {token_id}")
            
            nft_metadata = {
                'token_id': token_id,
                'name': f'Credit Grade {credit_grade} NFT',
                'description': f'Zero-Knowledge Proof based credit grade NFT for customer {customer_id}',
                'image': f'https://api.example.com/nft/{token_id}/image',
                'attributes': [
                    {
                        'trait_type': 'Credit Grade',
                        'value': credit_grade
                    },
                    {
                        'trait_type': 'Max Loan Amount',
                        'value': max_loan_amount
                    },
                    {
                        'trait_type': 'Issuer',
                        'value': 'EXTERNAL_AGENCY_001'
                    },
                    {
                        'trait_type': 'Issue Date',
                        'value': issue_date
                    },
                    {
                        'trait_type': 'Expiry Date',
                        'value': expiry_date
                    },
                    {
                        'trait_type': 'Validity Period',
                        'value': '30 days'
                    }
                ],
                'proof_id': proof_data['proof_id'],
                'customer_id': customer_id,
                'customer_address': customer_address,
                'issue_date': issue_date,
                'expiry_date': expiry_date,
                'is_valid': True
            }
            
            # NFT 저장
            save_nft(customer_id, customer_address, nft_metadata)
            print(f"🏛️ [EXTERNAL] NFT 발행 완료: {token_id}")
            print(f"🏛️ [EXTERNAL] 블록체인 주소: {customer_address}")
            print(f"🏛️ [EXTERNAL] 유효기간: {issue_date} ~ {expiry_date}")
        else:
            print(f"🏛️ [EXTERNAL] 기존 NFT 재사용: {token_id}")
            print(f"🏛️ [EXTERNAL] ZK-Proof 및 NFT 생성 생략")
        
        # credit_score 처리 (재사용 시에는 NFT에서 추출, 새로 생성 시에는 customer_info에서)
        if existing_nft and is_nft_valid(existing_nft):
            # 재사용 시: NFT에서 credit_score 추출 (실제로는 NFT에 저장되어 있어야 함)
            credit_score = 750  # Mock 값 (실제로는 NFT에서 추출)
        else:
            # 새로 생성 시: customer_info에서 가져옴
            credit_score = customer_info['credit_score']
        
        response = {
            'inquiry_id': inquiry_id,
            'request_id': request_id,  # 대출 요청 ID 연결
            'customer_id': customer_id,
            'customer_name': customer_name,
            'credit_score': credit_score,
            'credit_grade': credit_grade,
            'max_loan_amount': max_loan_amount,
            'requested_amount': requested_amount,
            'approval_eligible': requested_amount <= max_loan_amount,
            'inquiry_timestamp': datetime.now().isoformat(),
            'agency_id': 'EXTERNAL_AGENCY_001',
            'proof_id': proof_data['proof_id'],
            'token_id': token_id,
            'nft_metadata': nft_metadata,
            'blockchain_tx_hash': f'0x{hashlib.sha256(token_id.encode()).hexdigest()[:64]}',
            'status': 'completed'
        }
        
        approval_status = "승인 가능" if requested_amount <= max_loan_amount else "승인 불가"
        print(f"🏛️ [EXTERNAL] 승인 가능 여부: {approval_status}")
        print(f"🏛️ [EXTERNAL] 은행으로 결과 전송 완료")
        print(f"🏛️ [EXTERNAL] ==========================================")
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@external_bp.route('/generate-proof', methods=['POST'])
def generate_proof():
    """
    신용정보를 기반으로 ZK-Proof를 생성합니다.
    
    Request Body:
    {
        "inquiry_id": "조회 ID",
        "customer_id": "고객 ID",
        "credit_score": 750,
        "credit_grade": "B",
        "max_loan_amount": 50000000
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['customer_id', 'credit_score', 'credit_grade', 'max_loan_amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        inquiry_id = data.get('inquiry_id', f'INQ_{data["customer_id"]}_{int(datetime.now().timestamp())}')
        customer_id = data['customer_id']
        credit_score = data['credit_score']
        credit_grade = data['credit_grade']
        max_loan_amount = data['max_loan_amount']
        
        # 실제 구현에서는 ZoKrates를 사용하여 ZK-Proof를 생성합니다
        # 여기서는 Mock proof를 생성합니다
        proof_data = {
            'proof_id': f'PROOF_{inquiry_id}',
            'customer_id': customer_id,
            'credit_score_hash': hashlib.sha256(str(credit_score).encode()).hexdigest(),
            'credit_grade_hash': hashlib.sha256(credit_grade.encode()).hexdigest(),
            'max_loan_amount_hash': hashlib.sha256(str(max_loan_amount).encode()).hexdigest(),
            'proof_timestamp': datetime.now().isoformat(),
            'zk_proof': {
                'a': ['0x1234567890abcdef', '0xabcdef1234567890'],
                'b': [['0x1111111111111111', '0x2222222222222222'], ['0x3333333333333333', '0x4444444444444444']],
                'c': ['0x5555555555555555', '0x6666666666666666']
            }
        }
        
        response = {
            'proof_id': proof_data['proof_id'],
            'status': 'generated',
            'proof_data': proof_data,
            'message': 'ZK-Proof가 성공적으로 생성되었습니다.'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@external_bp.route('/mint-nft', methods=['POST'])
def mint_nft():
    """
    ZK-Proof를 기반으로 NFT를 발행합니다.
    
    Request Body:
    {
        "proof_id": "Proof ID",
        "customer_id": "고객 ID",
        "credit_grade": "B",
        "max_loan_amount": 50000000,
        "customer_address": "0x..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['customer_id', 'credit_grade', 'max_loan_amount', 'customer_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        proof_id = data.get('proof_id', f'PROOF_{data["customer_id"]}_{int(datetime.now().timestamp())}')
        customer_id = data['customer_id']
        credit_grade = data['credit_grade']
        max_loan_amount = data['max_loan_amount']
        customer_address = data['customer_address']
        
        # 실제 구현에서는 블록체인에 NFT를 발행합니다
        # 여기서는 Mock NFT 발행을 시뮬레이션합니다
        token_id = f'NFT_{proof_id}_{int(datetime.now().timestamp())}'
        
        nft_metadata = {
            'token_id': token_id,
            'name': f'Credit Grade {credit_grade} NFT',
            'description': f'Zero-Knowledge Proof based credit grade NFT for customer {customer_id}',
            'image': f'https://api.example.com/nft/{token_id}/image',
            'attributes': [
                {
                    'trait_type': 'Credit Grade',
                    'value': credit_grade
                },
                {
                    'trait_type': 'Max Loan Amount',
                    'value': max_loan_amount
                },
                {
                    'trait_type': 'Issuer',
                    'value': 'EXTERNAL_AGENCY_001'
                },
                {
                    'trait_type': 'Issue Date',
                    'value': datetime.now().isoformat()
                }
            ],
            'proof_id': proof_id,
            'customer_id': customer_id,
            'customer_address': customer_address
        }
        
        response = {
            'token_id': token_id,
            'status': 'minted',
            'nft_metadata': nft_metadata,
            'blockchain_tx_hash': f'0x{hashlib.sha256(token_id.encode()).hexdigest()[:64]}',
            'message': 'NFT가 성공적으로 발행되었습니다.'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@external_bp.route('/proof/<proof_id>', methods=['GET'])
def get_proof(proof_id):
    """
    특정 ZK-Proof 정보를 조회합니다.
    """
    try:
        # 실제 구현에서는 데이터베이스에서 proof 정보를 조회합니다
        # 여기서는 Mock 응답을 반환합니다
        mock_proof = {
            'proof_id': proof_id,
            'customer_id': 'CUST_001',
            'credit_score_hash': hashlib.sha256('750'.encode()).hexdigest(),
            'credit_grade_hash': hashlib.sha256('B'.encode()).hexdigest(),
            'max_loan_amount_hash': hashlib.sha256('50000000'.encode()).hexdigest(),
            'proof_timestamp': '2024-01-15T10:30:00Z',
            'status': 'verified'
        }
        
        return jsonify(mock_proof), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@external_bp.route('/my-nft', methods=['POST'])
def get_my_nft():
    """
    고객이 자신의 NFT를 조회합니다.
    
    Request Body:
    {
        "customer_id": "고객 ID",
        "customer_address": "블록체인 주소"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['customer_id', 'customer_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        customer_id = data['customer_id']
        customer_address = data['customer_address']
        
        print(f"🏛️ [EXTERNAL] NFT 조회 요청: {customer_id} ({customer_address})")
        
        # 기존 NFT 조회
        existing_nft = get_existing_nft(customer_id, customer_address)
        
        if not existing_nft:
            return jsonify({
                'status': 'not_found',
                'message': '해당 고객의 NFT를 찾을 수 없습니다.',
                'customer_id': customer_id,
                'customer_address': customer_address
            }), 404
        
        # 유효기간 확인
        is_valid = is_nft_valid(existing_nft)
        
        if not is_valid:
            print(f"🏛️ [EXTERNAL] NFT 유효기간 만료: {existing_nft['token_id']}")
            return jsonify({
                'status': 'expired',
                'message': 'NFT 유효기간이 만료되었습니다. 새로운 신용정보 조회가 필요합니다.',
                'nft_data': existing_nft,
                'customer_id': customer_id,
                'customer_address': customer_address
            }), 200
        
        print(f"🏛️ [EXTERNAL] NFT 조회 완료: {existing_nft['token_id']}")
        
        return jsonify({
            'status': 'valid',
            'message': 'NFT가 유효합니다.',
            'nft_data': existing_nft,
            'customer_id': customer_id,
            'customer_address': customer_address
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 