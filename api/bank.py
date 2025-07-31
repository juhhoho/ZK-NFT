"""
은행 관련 API 엔드포인트
대출 요청 처리, 신용등급 기준 조회, NFT 검증 등의 기능을 제공합니다.
"""

from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

bank_bp = Blueprint('bank', __name__)

# Mock 데이터 로드
def load_bank_criteria():
    """은행의 신용등급 기준을 로드합니다."""
    try:
        with open('data/bank_criteria.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 기본 기준 반환
        return {
            "credit_score_ranges": {
                "A": {"min": 800, "max": 1000, "description": "최우량"},
                "B": {"min": 700, "max": 799, "description": "우량"},
                "C": {"min": 600, "max": 699, "description": "보통"},
                "D": {"min": 500, "max": 599, "description": "주의"},
                "E": {"min": 0, "max": 499, "description": "위험"}
            },
            "loan_limits": {
                "A": 100000000,  # 1억원
                "B": 50000000,   # 5천만원
                "C": 20000000,   # 2천만원
                "D": 5000000,    # 5백만원
                "E": 0
            }
        }

@bank_bp.route('/loan-request', methods=['POST'])
def loan_request():
    """
    대출 요청을 처리합니다.
    
    Request Body:
    {
        "customer_id": "고객 ID",
        "customer_name": "고객명",
        "requested_amount": 10000000,
        "purpose": "대출 목적"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['customer_id', 'customer_name', 'requested_amount', 'purpose', 'customer_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        customer_id = data['customer_id']
        customer_name = data['customer_name']
        requested_amount = data['requested_amount']
        purpose = data['purpose']
        customer_address = data['customer_address']
        
        # 외부기관에 신용정보 조회 요청을 위한 정보 생성
        request_id = f'REQ_{customer_id}_{int(datetime.now().timestamp())}'
        inquiry_request = {
            'request_id': request_id,  # 대출 요청 ID 추가
            'customer_id': customer_id,
            'customer_name': customer_name,
            'requested_amount': requested_amount,
            'purpose': purpose,
            'customer_address': customer_address,  # NFT 발행용 주소
            'request_timestamp': datetime.now().isoformat(), # 요청시간 - 타임스탬프자동생성
            'bank_id': "BANK_001" # 은행id - 목업데이터 고정
        }
        
        print(f"🏦 [BANK] 대출 요청 접수: {customer_name}({customer_id}) - {requested_amount:,}원")
        print(f"🏦 [BANK] Request ID 생성: {request_id}")
        print(f"🏦 [BANK] 외부기관 요청 준비 완료")
        
        # 실제 외부기관 API 호출
        import requests
        
        try:
            print(f"🏦 [BANK] 외부기관 API 호출 시작...")
            # 외부기관 API 호출
            external_response = requests.post(
                'http://localhost:5000/api/external/credit-inquiry',
                json=inquiry_request,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            print(f"🏦 [BANK] 외부기관 API 응답 수신: {external_response.status_code}")
            
            if external_response.status_code == 200:
                external_data = external_response.json()
                print(f"🏦 [BANK] 외부기관 데이터 수신 완료")
                print(f"🏦 [BANK] 신용등급: {external_data['credit_grade']}, 최대대출한도: {external_data['max_loan_amount']:,}원")
                print(f"🏦 [BANK] NFT 토큰 ID: {external_data['token_id']}")
                
                # 외부기관에서 받은 NFT 정보로 대출 승인 여부 결정
                if external_data['approval_eligible']:
                    approval_status = 'approved'
                    message = f'대출이 승인되었습니다. NFT 토큰 ID: {external_data["token_id"]}'
                    print(f"🏦 [BANK] 대출 승인 결정: {requested_amount:,}원 승인")
                else:
                    approval_status = 'rejected'
                    message = f'신용등급 기준에 미달하여 대출이 거절되었습니다. 최대 대출 가능 금액: {external_data["max_loan_amount"]:,}원'
                    print(f"🏦 [BANK] 대출 거절 결정: 신용등급 기준 미달")
                
                response = {
                    'status': 'completed',
                    'request_id': request_id,
                    'approval_status': approval_status,
                    'message': message,
                    'nft_token_id': external_data['token_id'],
                    'credit_grade': external_data['credit_grade'],
                    'max_loan_amount': external_data['max_loan_amount'],
                    'approved_amount': min(requested_amount, external_data['max_loan_amount']),
                    'completed_at': datetime.now().isoformat(),
                    'external_response': external_data
                }
                print(f"🏦 [BANK] 고객에게 최종 결과 반환: {approval_status}")
                print(f"🏦 [BANK] ==========================================")
            else:
                # 외부기관 API 호출 실패
                response = {
                    'status': 'error',
                    'request_id': request_id,
                    'message': '외부기관 신용정보 조회 중 오류가 발생했습니다.',
                    'error_code': external_response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            # 네트워크 오류 등
            response = {
                'status': 'error',
                'request_id': request_id,
                'message': '외부기관 연결 중 오류가 발생했습니다.',
                'error': str(e)
            }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bank_bp.route('/credit-criteria', methods=['GET'])
def get_credit_criteria():
    """
    은행의 신용등급 기준을 조회합니다.
    """
    try:
        criteria = load_bank_criteria()
        
        response = {
            'bank_id': 'BANK_001',
            'bank_name': 'zk-nft 은행',
            'criteria': criteria,
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bank_bp.route('/verify-nft', methods=['POST'])
def verify_nft():
    """
    NFT를 검증하여 대출 승인 여부를 결정합니다.
    
    Request Body:
    {
        "token_id": "NFT 토큰 ID",
        "requested_amount": 10000000
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['token_id', 'customer_address', 'requested_amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        token_id = data['token_id']
        requested_amount = data['requested_amount']
        
        # 실제 구현에서는 블록체인에서 NFT 정보를 조회하고 검증합니다
        # 여기서는 Mock 응답을 반환합니다
        mock_nft_data = {
            'token_id': token_id,
            'credit_grade': 'B',
            'credit_score': 750,
            'max_loan_amount': 50000000,
            'issued_date': '2024-01-15T10:30:00Z',
            'issuer': 'EXTERNAL_AGENCY_001'
        }
        
        # 대출 승인 여부 결정
        if requested_amount <= mock_nft_data['max_loan_amount']:
            approval_status = 'approved'
            message = '대출이 승인되었습니다.'
        else:
            approval_status = 'rejected'
            message = f'요청 금액이 신용등급 한도를 초과합니다. 최대 대출 가능 금액: {mock_nft_data["max_loan_amount"]:,}원'
        
        response = {
            'token_id': token_id,
            'nft_data': mock_nft_data,
            'requested_amount': requested_amount,
            'approval_status': approval_status,
            'message': message,
            'verified_at': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bank_bp.route('/loan-status/<request_id>', methods=['GET'])
def get_loan_status(request_id):
    """
    대출 요청의 처리 상태를 조회합니다.
    """
    try:
        # 실제 구현에서는 데이터베이스에서 상태를 조회합니다
        # 여기서는 Mock 응답을 반환합니다
        mock_status = {
            'request_id': request_id,
            'status': 'completed',
            'nft_token_id': f'NFT_{request_id}',
            'credit_grade': 'B',
            'approved_amount': 50000000,
            'created_at': '2024-01-15T10:00:00Z',
            'completed_at': '2024-01-15T10:30:00Z'
        }
        
        return jsonify(mock_status), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 