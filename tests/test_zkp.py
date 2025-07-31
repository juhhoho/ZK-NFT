"""
Zero-Knowledge Proof 테스트
zk-nft 시스템의 ZKP 관련 기능들을 테스트합니다.
"""

import pytest
import json
import hashlib
from datetime import datetime
from utils.zkp_utils import ZKPUtils

class TestZKPUtils:
    """ZKP 유틸리티 테스트"""
    
    def setup_method(self):
        """테스트 설정"""
        self.zkp_utils = ZKPUtils()
    
    def test_create_credit_score_proof(self):
        """신용등급 ZK-Proof 생성 테스트"""
        credit_score = 750
        credit_grade = "B"
        max_loan_amount = 50000000
        
        result = self.zkp_utils.create_credit_score_proof(
            credit_score, credit_grade, max_loan_amount
        )
        
        assert result['status'] == 'success'
        assert 'proof_data' in result
        
        proof_data = result['proof_data']
        assert 'proof_id' in proof_data
        assert 'credit_score_hash' in proof_data
        assert 'credit_grade_hash' in proof_data
        assert 'max_loan_amount_hash' in proof_data
        assert 'zk_proof' in proof_data
        assert 'public_inputs' in proof_data
        
        # 해시값 검증
        expected_credit_score_hash = hashlib.sha256(str(credit_score).encode()).hexdigest()
        expected_credit_grade_hash = hashlib.sha256(credit_grade.encode()).hexdigest()
        expected_max_loan_amount_hash = hashlib.sha256(str(max_loan_amount).encode()).hexdigest()
        
        assert proof_data['credit_score_hash'] == expected_credit_score_hash
        assert proof_data['credit_grade_hash'] == expected_credit_grade_hash
        assert proof_data['max_loan_amount_hash'] == expected_max_loan_amount_hash
    
    def test_verify_credit_score_proof_valid(self):
        """유효한 신용등급 ZK-Proof 검증 테스트"""
        # 유효한 proof 데이터 생성
        proof_data = {
            'zk_proof': {
                'a': ['0x1234567890abcdef', '0xabcdef1234567890'],
                'b': [['0x1111111111111111', '0x2222222222222222'], 
                      ['0x3333333333333333', '0x4444444444444444']],
                'c': ['0x5555555555555555', '0x6666666666666666']
            },
            'public_inputs': [
                hashlib.sha256('750'.encode()).hexdigest(),
                hashlib.sha256('B'.encode()).hexdigest(),
                hashlib.sha256('50000000'.encode()).hexdigest()
            ]
        }
        
        result = self.zkp_utils.verify_credit_score_proof(proof_data)
        
        assert result['status'] == 'success'
        assert result['is_valid'] == True
    
    def test_verify_credit_score_proof_invalid_structure(self):
        """잘못된 구조의 ZK-Proof 검증 테스트"""
        # 잘못된 구조의 proof 데이터
        invalid_proof_data = {
            'zk_proof': {
                'a': ['0x1234567890abcdef']  # 길이가 2가 아님
            },
            'public_inputs': [
                hashlib.sha256('750'.encode()).hexdigest()
            ]
        }
        
        result = self.zkp_utils.verify_credit_score_proof(invalid_proof_data)
        
        assert result['status'] == 'error'
        assert result['is_valid'] == False
    
    def test_verify_credit_score_proof_missing_fields(self):
        """필수 필드가 누락된 ZK-Proof 검증 테스트"""
        # 필수 필드가 누락된 proof 데이터
        incomplete_proof_data = {
            'zk_proof': {
                'a': ['0x1234567890abcdef', '0xabcdef1234567890'],
                'b': [['0x1111111111111111', '0x2222222222222222'], 
                      ['0x3333333333333333', '0x4444444444444444']],
                'c': ['0x5555555555555555', '0x6666666666666666']
            }
            # public_inputs 필드 누락
        }
        
        result = self.zkp_utils.verify_credit_score_proof(incomplete_proof_data)
        
        assert result['status'] == 'error'
        assert result['is_valid'] == False
    
    def test_credit_score_proof_consistency(self):
        """신용등급 ZK-Proof 일관성 테스트"""
        # 동일한 입력값으로 여러 번 proof 생성
        credit_score = 750
        credit_grade = "B"
        max_loan_amount = 50000000
        
        result1 = self.zkp_utils.create_credit_score_proof(
            credit_score, credit_grade, max_loan_amount
        )
        result2 = self.zkp_utils.create_credit_score_proof(
            credit_score, credit_grade, max_loan_amount
        )
        
        assert result1['status'] == 'success'
        assert result2['status'] == 'success'
        
        # 해시값은 동일해야 함
        proof_data1 = result1['proof_data']
        proof_data2 = result2['proof_data']
        
        assert proof_data1['credit_score_hash'] == proof_data2['credit_score_hash']
        assert proof_data1['credit_grade_hash'] == proof_data2['credit_grade_hash']
        assert proof_data1['max_loan_amount_hash'] == proof_data2['max_loan_amount_hash']
    
    def test_different_credit_grades(self):
        """다양한 신용등급에 대한 ZK-Proof 생성 테스트"""
        test_cases = [
            (920, "A", 100000000),
            (750, "B", 50000000),
            (650, "C", 20000000),
            (580, "D", 5000000),
            (450, "E", 0)
        ]
        
        for credit_score, credit_grade, max_loan_amount in test_cases:
            result = self.zkp_utils.create_credit_score_proof(
                credit_score, credit_grade, max_loan_amount
            )
            
            assert result['status'] == 'success'
            
            proof_data = result['proof_data']
            expected_credit_score_hash = hashlib.sha256(str(credit_score).encode()).hexdigest()
            expected_credit_grade_hash = hashlib.sha256(credit_grade.encode()).hexdigest()
            expected_max_loan_amount_hash = hashlib.sha256(str(max_loan_amount).encode()).hexdigest()
            
            assert proof_data['credit_score_hash'] == expected_credit_score_hash
            assert proof_data['credit_grade_hash'] == expected_credit_grade_hash
            assert proof_data['max_loan_amount_hash'] == expected_max_loan_amount_hash
    
    def test_proof_id_uniqueness(self):
        """Proof ID 고유성 테스트"""
        credit_score = 750
        credit_grade = "B"
        max_loan_amount = 50000000
        
        # 여러 번 proof 생성하여 ID 고유성 확인
        proof_ids = set()
        
        for _ in range(5):
            result = self.zkp_utils.create_credit_score_proof(
                credit_score, credit_grade, max_loan_amount
            )
            
            assert result['status'] == 'success'
            proof_id = result['proof_data']['proof_id']
            proof_ids.add(proof_id)
        
        # 모든 proof ID가 고유해야 함
        assert len(proof_ids) == 5
    
    def test_timestamp_format(self):
        """타임스탬프 형식 테스트"""
        credit_score = 750
        credit_grade = "B"
        max_loan_amount = 50000000
        
        result = self.zkp_utils.create_credit_score_proof(
            credit_score, credit_grade, max_loan_amount
        )
        
        assert result['status'] == 'success'
        
        proof_data = result['proof_data']
        timestamp = proof_data['proof_timestamp']
        
        # ISO 8601 형식 검증
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")

class TestZKPIntegration:
    """ZKP 통합 테스트"""
    
    def setup_method(self):
        """테스트 설정"""
        self.zkp_utils = ZKPUtils()
    
    def test_end_to_end_zkp_flow(self):
        """ZKP 전체 흐름 테스트"""
        # 1. ZK-Proof 생성
        credit_score = 750
        credit_grade = "B"
        max_loan_amount = 50000000
        
        create_result = self.zkp_utils.create_credit_score_proof(
            credit_score, credit_grade, max_loan_amount
        )
        
        assert create_result['status'] == 'success'
        proof_data = create_result['proof_data']
        
        # 2. ZK-Proof 검증
        verify_result = self.zkp_utils.verify_credit_score_proof(proof_data)
        
        assert verify_result['status'] == 'success'
        assert verify_result['is_valid'] == True
        
        # 3. 검증된 proof 데이터의 무결성 확인
        assert proof_data['credit_score_hash'] == hashlib.sha256(str(credit_score).encode()).hexdigest()
        assert proof_data['credit_grade_hash'] == hashlib.sha256(credit_grade.encode()).hexdigest()
        assert proof_data['max_loan_amount_hash'] == hashlib.sha256(str(max_loan_amount).encode()).hexdigest()
    
    def test_zkp_with_different_inputs(self):
        """다양한 입력값으로 ZKP 통합 테스트"""
        test_cases = [
            (920, "A", 100000000),
            (750, "B", 50000000),
            (650, "C", 20000000),
            (580, "D", 5000000),
            (450, "E", 0)
        ]
        
        for credit_score, credit_grade, max_loan_amount in test_cases:
            # ZK-Proof 생성
            create_result = self.zkp_utils.create_credit_score_proof(
                credit_score, credit_grade, max_loan_amount
            )
            
            assert create_result['status'] == 'success'
            proof_data = create_result['proof_data']
            
            # ZK-Proof 검증
            verify_result = self.zkp_utils.verify_credit_score_proof(proof_data)
            
            assert verify_result['status'] == 'success'
            assert verify_result['is_valid'] == True
            
            # 해시값 검증
            expected_credit_score_hash = hashlib.sha256(str(credit_score).encode()).hexdigest()
            expected_credit_grade_hash = hashlib.sha256(credit_grade.encode()).hexdigest()
            expected_max_loan_amount_hash = hashlib.sha256(str(max_loan_amount).encode()).hexdigest()
            
            assert proof_data['credit_score_hash'] == expected_credit_score_hash
            assert proof_data['credit_grade_hash'] == expected_credit_grade_hash
            assert proof_data['max_loan_amount_hash'] == expected_max_loan_amount_hash

if __name__ == '__main__':
    pytest.main([__file__]) 