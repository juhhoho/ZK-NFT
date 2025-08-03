"""
실제 블록체인 연동을 위한 유틸리티 함수들
Web3를 사용한 실제 블록체인 상호작용 기능을 제공합니다.
"""

import os
import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from web3 import Web3
from eth_account import Account
import secrets
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class RealBlockchainUtils:
    """실제 블록체인 유틸리티 클래스"""
    
    def __init__(self):
        """
        블록체인 유틸리티 초기화
        환경 변수에서 설정을 로드합니다.
        """
        self.blockchain_url = os.getenv('BLOCKCHAIN_URL', 'http://localhost:8545')
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        self.deployer_address = os.getenv('DEPLOYER_ADDRESS')
        self.network_id = int(os.getenv('NETWORK_ID', '1337'))
        
        # Web3 연결
        self.w3 = Web3(Web3.HTTPProvider(self.blockchain_url))
        
        # 컨트랙트 ABI 로드
        self.contract_abi = self._load_contract_abi()
        
        # 컨트랙트 인스턴스 생성
        if self.contract_address and self.contract_abi:
            self.contract = self.w3.eth.contract(
                address=self.contract_address, 
                abi=self.contract_abi
            )
        else:
            self.contract = None
            
        print(f"🔗 Blockchain connected: {self.blockchain_url}")
        print(f"📋 Contract address: {self.contract_address}")
        
    def _load_contract_abi(self) -> List:
        """
        컨트랙트 ABI를 로드합니다.
        
        Returns:
            컨트랙트 ABI
        """
        try:
            # Hardhat artifacts에서 ABI 로드
            artifacts_path = os.path.join(
                os.path.dirname(__file__), 
                '../blockchain/artifacts/contracts/CreditGradeNFT.sol/CreditGradeNFT.json'
            )
            
            if os.path.exists(artifacts_path):
                with open(artifacts_path, 'r') as f:
                    contract_json = json.load(f)
                    return contract_json['abi']
            else:
                print("⚠️  Contract ABI not found. Using minimal ABI.")
                # 최소한의 ABI (기본 함수들만)
                return [
                    {
                        "inputs": [
                            {"internalType": "address", "name": "to", "type": "address"},
                            {"internalType": "string", "name": "tokenURI", "type": "string"},
                            {"internalType": "string", "name": "creditGrade", "type": "string"},
                            {"internalType": "uint256", "name": "maxLoanAmount", "type": "uint256"},
                            {"internalType": "string", "name": "proofId", "type": "string"},
                            {"internalType": "string", "name": "customerId", "type": "string"}
                        ],
                        "name": "mintCreditGradeNFT",
                        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                        "stateMutability": "nonpayable",
                        "type": "function"
                    },
                    {
                        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
                        "name": "getCreditGradeData",
                        "outputs": [
                            {
                                "components": [
                                    {"internalType": "string", "name": "creditGrade", "type": "string"},
                                    {"internalType": "uint256", "name": "maxLoanAmount", "type": "uint256"},
                                    {"internalType": "string", "name": "proofId", "type": "string"},
                                    {"internalType": "string", "name": "customerId", "type": "string"},
                                    {"internalType": "uint256", "name": "issuedAt", "type": "uint256"},
                                    {"internalType": "bool", "name": "isValid", "type": "bool"}
                                ],
                                "internalType": "struct CreditGradeNFT.CreditGradeData",
                                "name": "",
                                "type": "tuple"
                            }
                        ],
                        "stateMutability": "view",
                        "type": "function"
                    },
                    {
                        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
                        "name": "isValidNFT",
                        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                        "stateMutability": "view",
                        "type": "function"
                    },
                    {
                        "inputs": [
                            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                            {"internalType": "uint256", "name": "requestedAmount", "type": "uint256"}
                        ],
                        "name": "checkLoanEligibility",
                        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                        "stateMutability": "view",
                        "type": "function"
                    }
                ]
        except Exception as e:
            print(f"❌ Error loading contract ABI: {e}")
            return []
    
    def connect_to_blockchain(self) -> Dict:
        """
        블록체인에 연결합니다.
        
        Returns:
            연결 결과
        """
        try:
            # Web3 연결 확인 (버전에 따라 다른 메서드 사용)
            try:
                is_connected = self.w3.is_connected()
            except AttributeError:
                # Web3.py v6+ 에서는 is_connected() 대신 다른 방법 사용
                try:
                    self.w3.eth.block_number
                    is_connected = True
                except:
                    is_connected = False
            
            if is_connected:
                latest_block = self.w3.eth.block_number
                return {
                    'status': 'success',
                    'message': 'Successfully connected to blockchain',
                    'network_id': self.w3.eth.chain_id,
                    'latest_block': latest_block,
                    'contract_address': self.contract_address,
                    'is_contract_deployed': self.contract is not None
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to connect to blockchain'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}',
                'error': str(e)
            }
    
    def create_account(self) -> Dict:
        """
        새로운 이더리움 계정을 생성합니다.
        
        Returns:
            생성된 계정 정보
        """
        try:
            # 새로운 개인키 생성
            private_key = "0x" + secrets.token_hex(32)
            account = Account.from_key(private_key)
            
            return {
                'status': 'success',
                'message': 'Account created successfully',
                'address': account.address,
                'private_key': private_key
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Account creation error: {str(e)}',
                'error': str(e)
            }
    
    def get_balance(self, address: str) -> Dict:
        """
        특정 주소의 잔액을 조회합니다.
        
        Args:
            address: 조회할 주소
            
        Returns:
            잔액 정보
        """
        try:
            # Web3.py 버전 호환성을 위한 주소 검증
            try:
                if not self.w3.is_address(address):
                    return {
                        'status': 'error',
                        'message': 'Invalid address format'
                    }
            except AttributeError:
                # Web3.py v6+ 에서는 다른 방법으로 주소 검증
                if not address.startswith('0x') or len(address) != 42:
                    return {
                        'status': 'error',
                        'message': 'Invalid address format'
                    }
            
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            return {
                'status': 'success',
                'address': address,
                'balance_wei': balance_wei,
                'balance_eth': float(balance_eth)
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Balance check error: {str(e)}',
                'error': str(e)
            }
    
    def mint_credit_grade_nft(self, to_address: str, credit_grade: str,
                             max_loan_amount: int, proof_id: str, 
                             customer_id: str, minter_private_key: str) -> Dict:
        """
        신용등급 NFT를 실제로 발행합니다.
        
        Args:
            to_address: NFT 수신자 주소
            credit_grade: 신용등급
            max_loan_amount: 최대 대출 가능 금액
            proof_id: ZK-Proof ID
            customer_id: 고객 ID
            minter_private_key: 발행자 개인키
            
        Returns:
            발행 결과
        """
        try:
            if not self.contract:
                return {
                    'status': 'error',
                    'message': 'Contract not deployed or ABI not loaded'
                }
            
            # 발행자 주소 가져오기
            minter_account = Account.from_key(minter_private_key)
            minter_address = minter_account.address
            
            # NFT 메타데이터 URI 생성
            token_uri = self._create_token_uri(credit_grade, max_loan_amount, proof_id, customer_id)
            
            # 가스 추정
            gas_estimate = self.contract.functions.mintCreditGradeNFT(
                to_address, token_uri, credit_grade, max_loan_amount, proof_id, customer_id
            ).estimate_gas({'from': minter_address})
            
            # 트랜잭션 구성
            transaction = self.contract.functions.mintCreditGradeNFT(
                to_address, token_uri, credit_grade, max_loan_amount, proof_id, customer_id
            ).build_transaction({
                'from': minter_address,
                'gas': gas_estimate + 50000,  # 여유분 추가
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(minter_address)
            })
            
            # 트랜잭션 서명
            signed_txn = self.w3.eth.account.sign_transaction(transaction, minter_private_key)
            
            # 트랜잭션 전송
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # 트랜잭션 영수증 대기
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # 발행된 토큰 ID 조회 (이벤트에서 추출)
            token_id = self._get_token_id_from_receipt(tx_receipt)
            
            return {
                'status': 'success',
                'message': 'Credit Grade NFT minted successfully',
                'token_id': token_id,
                'to_address': to_address,
                'transaction_hash': tx_hash.hex(),
                'gas_used': tx_receipt.gasUsed,
                'block_number': tx_receipt.blockNumber,
                'credit_grade': credit_grade,
                'max_loan_amount': max_loan_amount,
                'proof_id': proof_id,
                'customer_id': customer_id
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'NFT minting error: {str(e)}',
                'error': str(e)
            }
    
    def _create_token_uri(self, credit_grade: str, max_loan_amount: int,
                         proof_id: str, customer_id: str) -> str:
        """
        NFT 메타데이터 URI를 생성합니다.
        
        Args:
            credit_grade: 신용등급
            max_loan_amount: 최대 대출 가능 금액
            proof_id: ZK-Proof ID
            customer_id: 고객 ID
            
        Returns:
            메타데이터 URI
        """
        metadata = {
            'name': f'Credit Grade {credit_grade} NFT',
            'description': f'Zero-Knowledge Proof based credit grade NFT for customer {customer_id}',
            'image': f'https://api.example.com/nft/{proof_id}/image',
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
                    'trait_type': 'Proof ID',
                    'value': proof_id
                },
                {
                    'trait_type': 'Customer ID',
                    'value': customer_id
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
            'external_url': f'https://api.example.com/nft/{proof_id}'
        }
        
        # 실제로는 IPFS나 중앙화된 스토리지에 업로드해야 함
        # 여기서는 간단히 JSON 문자열로 반환
        return json.dumps(metadata)
    
    def _get_token_id_from_receipt(self, receipt) -> int:
        """
        트랜잭션 영수증에서 토큰 ID를 추출합니다.
        
        Args:
            receipt: 트랜잭션 영수증
            
        Returns:
            토큰 ID
        """
        try:
            # 이벤트 로그에서 토큰 ID 추출
            for log in receipt.logs:
                if log.address.lower() == self.contract_address.lower():
                    # CreditGradeNFTMinted 이벤트 파싱
                    decoded_log = self.contract.events.CreditGradeNFTMinted().process_log(log)
                    if decoded_log:
                        return decoded_log['args']['tokenId']
            
            # 이벤트에서 찾지 못한 경우, 총 발행 수로 추정
            total_supply = self.contract.functions.totalSupply().call()
            return total_supply
            
        except Exception as e:
            print(f"Warning: Could not extract token ID from receipt: {e}")
            # 폴백: 타임스탬프 기반 ID 생성
            return int(datetime.now().timestamp())
    
    def get_nft_info(self, token_id: int) -> Dict:
        """
        NFT 정보를 조회합니다.
        
        Args:
            token_id: 토큰 ID
            
        Returns:
            NFT 정보
        """
        try:
            if not self.contract:
                return {
                    'status': 'error',
                    'message': 'Contract not deployed or ABI not loaded'
                }
            
            # NFT 존재 여부 확인
            if not self.contract.functions._exists(token_id).call():
                return {
                    'status': 'error',
                    'message': 'NFT does not exist'
                }
            
            # 소유자 조회
            owner = self.contract.functions.ownerOf(token_id).call()
            
            # 신용등급 데이터 조회
            credit_data = self.contract.functions.getCreditGradeData(token_id).call()
            
            # 유효성 확인
            is_valid = self.contract.functions.isValidNFT(token_id).call()
            
            return {
                'status': 'success',
                'token_id': token_id,
                'owner': owner,
                'credit_grade': credit_data[0],
                'max_loan_amount': credit_data[1],
                'proof_id': credit_data[2],
                'customer_id': credit_data[3],
                'issued_at': credit_data[4],
                'is_valid': credit_data[5],
                'is_valid_nft': is_valid
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'NFT info retrieval error: {str(e)}',
                'error': str(e)
            }
    
    def check_loan_eligibility(self, token_id: int, requested_amount: int) -> Dict:
        """
        대출 자격을 확인합니다.
        
        Args:
            token_id: 토큰 ID
            requested_amount: 요청 대출 금액
            
        Returns:
            대출 자격 확인 결과
        """
        try:
            if not self.contract:
                return {
                    'status': 'error',
                    'message': 'Contract not deployed or ABI not loaded'
                }
            
            # 컨트랙트에서 대출 자격 확인
            is_eligible = self.contract.functions.checkLoanEligibility(token_id, requested_amount).call()
            
            # NFT 정보도 함께 조회
            nft_info = self.get_nft_info(token_id)
            
            return {
                'status': 'success',
                'token_id': token_id,
                'requested_amount': requested_amount,
                'is_eligible': is_eligible,
                'nft_info': nft_info
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Loan eligibility check error: {str(e)}',
                'error': str(e)
            }
    
    def get_customer_tokens(self, customer_id: str) -> Dict:
        """
        고객의 모든 토큰을 조회합니다.
        
        Args:
            customer_id: 고객 ID
            
        Returns:
            고객의 토큰 목록
        """
        try:
            if not self.contract:
                return {
                    'status': 'error',
                    'message': 'Contract not deployed or ABI not loaded'
                }
            
            # 고객의 토큰 ID 목록 조회
            token_ids = self.contract.functions.getCustomerTokens(customer_id).call()
            
            # 각 토큰의 상세 정보 조회
            tokens_info = []
            for token_id in token_ids:
                token_info = self.get_nft_info(token_id)
                if token_info['status'] == 'success':
                    tokens_info.append(token_info)
            
            return {
                'status': 'success',
                'customer_id': customer_id,
                'token_count': len(token_ids),
                'token_ids': token_ids,
                'tokens_info': tokens_info
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Customer tokens retrieval error: {str(e)}',
                'error': str(e)
            }

# 전역 블록체인 유틸리티 인스턴스
real_blockchain_utils = RealBlockchainUtils() 