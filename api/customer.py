"""
고객 관련 API 엔드포인트
NFT 정보 조회, NFT 전송 등의 기능을 제공합니다.
"""

from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/nft/<token_id>', methods=['GET'])
def get_nft_info(token_id):
    """
    특정 NFT의 정보를 조회합니다.
    """
    try:
        # 실제 구현에서는 블록체인에서 NFT 정보를 조회합니다
        # 여기서는 Mock NFT 정보를 반환합니다
        mock_nft_info = {
            'token_id': token_id,
            'name': 'Credit Grade B NFT',
            'description': 'Zero-Knowledge Proof based credit grade NFT',
            'image': f'https://api.example.com/nft/{token_id}/image',
            'attributes': [
                {
                    'trait_type': 'Credit Grade',
                    'value': 'B'
                },
                {
                    'trait_type': 'Max Loan Amount',
                    'value': 50000000
                },
                {
                    'trait_type': 'Issuer',
                    'value': 'EXTERNAL_AGENCY_001'
                },
                {
                    'trait_type': 'Issue Date',
                    'value': '2024-01-15T10:30:00Z'
                }
            ],
            'owner': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6',
            'proof_id': f'PROOF_{token_id}',
            'customer_id': 'CUST_001',
            'blockchain_tx_hash': f'0x{token_id[:64]}',
            'created_at': '2024-01-15T10:30:00Z'
        }
        
        return jsonify(mock_nft_info), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/transfer-nft', methods=['POST'])
def transfer_nft():
    """
    NFT를 다른 주소로 전송합니다.
    
    Request Body:
    {
        "token_id": "NFT 토큰 ID",
        "from_address": "0x...",
        "to_address": "0x...",
        "customer_signature": "서명 데이터"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['token_id', 'from_address', 'to_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        token_id = data['token_id']
        from_address = data['from_address']
        to_address = data['to_address']
        customer_signature = data.get('customer_signature', '')
        
        # 실제 구현에서는 블록체인에서 NFT 전송을 실행합니다
        # 여기서는 Mock 전송을 시뮬레이션합니다
        
        # 전송 성공 시뮬레이션
        transfer_success = True
        
        if transfer_success:
            response = {
                'token_id': token_id,
                'from_address': from_address,
                'to_address': to_address,
                'status': 'transferred',
                'blockchain_tx_hash': f'0x{token_id}_{int(datetime.now().timestamp())}',
                'transfer_timestamp': datetime.now().isoformat(),
                'message': 'NFT가 성공적으로 전송되었습니다.'
            }
            
            return jsonify(response), 200
        else:
            return jsonify({'error': 'NFT 전송에 실패했습니다.'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/my-nfts/<customer_address>', methods=['GET'])
def get_customer_nfts(customer_address):
    """
    특정 고객이 소유한 모든 NFT를 조회합니다.
    """
    try:
        # 실제 구현에서는 블록체인에서 고객의 NFT 목록을 조회합니다
        # 여기서는 Mock NFT 목록을 반환합니다
        mock_nfts = [
            {
                'token_id': 'NFT_PROOF_CUST_001_1705312200',
                'name': 'Credit Grade B NFT',
                'credit_grade': 'B',
                'max_loan_amount': 50000000,
                'issued_date': '2024-01-15T10:30:00Z',
                'issuer': 'EXTERNAL_AGENCY_001'
            },
            {
                'token_id': 'NFT_PROOF_CUST_001_1705312500',
                'name': 'Credit Grade A NFT',
                'credit_grade': 'A',
                'max_loan_amount': 100000000,
                'issued_date': '2024-01-15T11:15:00Z',
                'issuer': 'EXTERNAL_AGENCY_001'
            }
        ]
        
        response = {
            'customer_address': customer_address,
            'total_nfts': len(mock_nfts),
            'nfts': mock_nfts,
            'retrieved_at': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/nft/<token_id>/verify', methods=['GET', 'POST'])
def verify_nft_ownership(token_id):
    """
    NFT 소유권을 검증합니다.
    
    GET: ?address=0x...
    POST: {"customer_address": "0x...", "customer_signature": "서명 데이터"}
    """
    try:
        if request.method == 'GET':
            customer_address = request.args.get('address')
            if not customer_address:
                return jsonify({'error': 'Missing required parameter: address'}), 400
            customer_signature = ''
        else:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            required_fields = ['customer_address']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            customer_address = data['customer_address']
            customer_signature = data.get('customer_signature', '')
        
        # 실제 구현에서는 블록체인에서 NFT 소유권을 검증합니다
        # 여기서는 Mock 검증을 시뮬레이션합니다
        mock_owner = '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6'
        is_owner = customer_address.lower() == mock_owner.lower()
        
        response = {
            'token_id': token_id,
            'customer_address': customer_address,
            'is_owner': is_owner,
            'verified_at': datetime.now().isoformat(),
            'message': 'NFT 소유권이 확인되었습니다.' if is_owner else 'NFT 소유자가 아닙니다.'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/nft/<token_id>/loan-eligibility', methods=['GET', 'POST'])
def check_loan_eligibility(token_id):
    """
    NFT를 기반으로 대출 자격을 확인합니다.
    
    GET: ?address=0x...&amount=10000000
    POST: {"requested_amount": 10000000, "customer_address": "0x..."}
    """
    try:
        if request.method == 'GET':
            customer_address = request.args.get('address')
            requested_amount = request.args.get('amount')
            if not customer_address:
                return jsonify({'error': 'Missing required parameter: address'}), 400
            if not requested_amount:
                return jsonify({'error': 'Missing required parameter: amount'}), 400
            try:
                requested_amount = int(requested_amount)
            except ValueError:
                return jsonify({'error': 'Invalid amount parameter'}), 400
        else:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            required_fields = ['requested_amount', 'customer_address']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            requested_amount = data['requested_amount']
            customer_address = data['customer_address']
        
        # 실제 구현에서는 블록체인에서 NFT 정보를 조회하고 검증합니다
        # 여기서는 Mock 검증을 시뮬레이션합니다
        mock_nft_data = {
            'credit_grade': 'B',
            'max_loan_amount': 50000000,
            'owner': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6'
        }
        
        is_owner = customer_address.lower() == mock_nft_data['owner'].lower()
        is_eligible = requested_amount <= mock_nft_data['max_loan_amount']
        
        response = {
            'token_id': token_id,
            'customer_address': customer_address,
            'requested_amount': requested_amount,
            'is_owner': is_owner,
            'is_eligible': is_eligible and is_owner,
            'max_loan_amount': mock_nft_data['max_loan_amount'],
            'credit_grade': mock_nft_data['credit_grade'],
            'checked_at': datetime.now().isoformat(),
            'message': '대출 자격이 확인되었습니다.' if (is_eligible and is_owner) else '대출 자격이 없습니다.'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 