"""
블록체인 관련 유틸리티 함수들
Web3를 사용한 블록체인 상호작용 기능을 제공합니다.
"""

import os
import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from web3 import Web3
from eth_account import Account
import secrets

class BlockchainUtils:
    """블록체인 유틸리티 클래스"""
    
    def __init__(self, blockchain_url: str = "http://localhost:8545"):
        """
        블록체인 유틸리티 초기화
        
        Args:
            blockchain_url: 블록체인 노드 URL
        """
        self.blockchain_url = blockchain_url
        self.w3 = Web3(Web3.HTTPProvider(blockchain_url))
        self.account = None
        
    def connect_to_blockchain(self) -> Dict:
        """
        블록체인에 연결합니다.
        
        Returns:
            연결 결과
        """
        try:
            if self.w3.is_connected():
                return {
                    'status': 'success',
                    'message': 'Successfully connected to blockchain',
                    'network_id': self.w3.eth.chain_id,
                    'latest_block': self.w3.eth.block_number
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
            if not self.w3.is_address(address):
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
    
    def deploy_nft_contract(self, contract_abi: List, contract_bytecode: str, 
                           deployer_address: str, deployer_private_key: str) -> Dict:
        """
        NFT 컨트랙트를 배포합니다.
        
        Args:
            contract_abi: 컨트랙트 ABI
            contract_bytecode: 컨트랙트 바이트코드
            deployer_address: 배포자 주소
            deployer_private_key: 배포자 개인키
            
        Returns:
            배포 결과
        """
        try:
            # 컨트랙트 객체 생성
            contract = self.w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
            
            # 가스 추정
            gas_estimate = contract.constructor().estimate_gas({'from': deployer_address})
            
            # 트랜잭션 구성
            transaction = contract.constructor().build_transaction({
                'from': deployer_address,
                'gas': gas_estimate,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(deployer_address)
            })
            
            # 트랜잭션 서명
            signed_txn = self.w3.eth.account.sign_transaction(transaction, deployer_private_key)
            
            # 트랜잭션 전송
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # 트랜잭션 영수증 대기
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'status': 'success',
                'message': 'NFT contract deployed successfully',
                'contract_address': tx_receipt.contractAddress,
                'transaction_hash': tx_hash.hex(),
                'gas_used': tx_receipt.gasUsed
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Contract deployment error: {str(e)}',
                'error': str(e)
            }
    
    def mint_nft(self, contract_address: str, contract_abi: List, 
                to_address: str, token_uri: str, minter_address: str, 
                minter_private_key: str) -> Dict:
        """
        NFT를 발행합니다.
        
        Args:
            contract_address: NFT 컨트랙트 주소
            contract_abi: 컨트랙트 ABI
            to_address: NFT 수신자 주소
            token_uri: NFT 메타데이터 URI
            minter_address: 발행자 주소
            minter_private_key: 발행자 개인키
            
        Returns:
            발행 결과
        """
        try:
            # 컨트랙트 인스턴스 생성
            contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
            
            # mint 함수 호출을 위한 트랜잭션 구성
            transaction = contract.functions.mint(to_address, token_uri).build_transaction({
                'from': minter_address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(minter_address)
            })
            
            # 트랜잭션 서명
            signed_txn = self.w3.eth.account.sign_transaction(transaction, minter_private_key)
            
            # 트랜잭션 전송
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # 트랜잭션 영수증 대기
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # 발행된 토큰 ID 조회
            token_id = contract.functions.tokenOfOwnerByIndex(to_address, 0).call()
            
            return {
                'status': 'success',
                'message': 'NFT minted successfully',
                'token_id': token_id,
                'to_address': to_address,
                'transaction_hash': tx_hash.hex(),
                'gas_used': tx_receipt.gasUsed
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'NFT minting error: {str(e)}',
                'error': str(e)
            }
    
    def get_nft_info(self, contract_address: str, contract_abi: List, 
                    token_id: int) -> Dict:
        """
        NFT 정보를 조회합니다.
        
        Args:
            contract_address: NFT 컨트랙트 주소
            contract_abi: 컨트랙트 ABI
            token_id: 토큰 ID
            
        Returns:
            NFT 정보
        """
        try:
            # 컨트랙트 인스턴스 생성
            contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
            
            # NFT 정보 조회
            owner = contract.functions.ownerOf(token_id).call()
            token_uri = contract.functions.tokenURI(token_id).call()
            
            return {
                'status': 'success',
                'token_id': token_id,
                'owner': owner,
                'token_uri': token_uri
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'NFT info retrieval error: {str(e)}',
                'error': str(e)
            }
    
    def transfer_nft(self, contract_address: str, contract_abi: List,
                    from_address: str, to_address: str, token_id: int,
                    from_private_key: str) -> Dict:
        """
        NFT를 전송합니다.
        
        Args:
            contract_address: NFT 컨트랙트 주소
            contract_abi: 컨트랙트 ABI
            from_address: 전송자 주소
            to_address: 수신자 주소
            token_id: 토큰 ID
            from_private_key: 전송자 개인키
            
        Returns:
            전송 결과
        """
        try:
            # 컨트랙트 인스턴스 생성
            contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
            
            # transfer 함수 호출을 위한 트랜잭션 구성
            transaction = contract.functions.transferFrom(from_address, to_address, token_id).build_transaction({
                'from': from_address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(from_address)
            })
            
            # 트랜잭션 서명
            signed_txn = self.w3.eth.account.sign_transaction(transaction, from_private_key)
            
            # 트랜잭션 전송
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # 트랜잭션 영수증 대기
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'status': 'success',
                'message': 'NFT transferred successfully',
                'token_id': token_id,
                'from_address': from_address,
                'to_address': to_address,
                'transaction_hash': tx_hash.hex(),
                'gas_used': tx_receipt.gasUsed
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'NFT transfer error: {str(e)}',
                'error': str(e)
            }
    
    def create_nft_metadata(self, credit_grade: str, max_loan_amount: int,
                           proof_id: str, customer_id: str) -> Dict:
        """
        NFT 메타데이터를 생성합니다.
        
        Args:
            credit_grade: 신용등급
            max_loan_amount: 최대 대출 가능 금액
            proof_id: ZK-Proof ID
            customer_id: 고객 ID
            
        Returns:
            NFT 메타데이터
        """
        try:
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
                'external_url': f'https://api.example.com/nft/{proof_id}'
            }
            
            return {
                'status': 'success',
                'metadata': metadata
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Metadata creation error: {str(e)}',
                'error': str(e)
            }
    
    def mock_nft_mint(self, customer_address: str, credit_grade: str,
                     max_loan_amount: int, proof_id: str) -> Dict:
        """
        Mock NFT 발행을 시뮬레이션합니다.
        
        Args:
            customer_address: 고객 주소
            credit_grade: 신용등급
            max_loan_amount: 최대 대출 가능 금액
            proof_id: ZK-Proof ID
            
        Returns:
            Mock 발행 결과
        """
        try:
            token_id = f'NFT_{proof_id}_{int(datetime.now().timestamp())}'
            
            # Mock 메타데이터 생성
            metadata_result = self.create_nft_metadata(
                credit_grade, max_loan_amount, proof_id, customer_address
            )
            
            if metadata_result['status'] == 'success':
                return {
                    'status': 'success',
                    'message': 'Mock NFT minted successfully',
                    'token_id': token_id,
                    'customer_address': customer_address,
                    'metadata': metadata_result['metadata'],
                    'blockchain_tx_hash': f'0x{hashlib.sha256(token_id.encode()).hexdigest()[:64]}',
                    'minted_at': datetime.now().isoformat()
                }
            else:
                return metadata_result
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Mock NFT minting error: {str(e)}',
                'error': str(e)
            }

# 전역 블록체인 유틸리티 인스턴스
blockchain_utils = BlockchainUtils() 