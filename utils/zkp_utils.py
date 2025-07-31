"""
Zero-Knowledge Proof 관련 유틸리티 함수들
ZoKrates를 사용한 ZK-Proof 생성 및 검증 기능을 제공합니다.
"""

import os
import json
import hashlib
import subprocess
import tempfile
import time
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class ZKPUtils:
    """Zero-Knowledge Proof 유틸리티 클래스"""
    
    def __init__(self, zokrates_image: str = "zokrates/zokrates:0.8.17"):
        """
        ZKP 유틸리티 초기화
        
        Args:
            zokrates_image: ZoKrates Docker 이미지명
        """
        self.zokrates_image = zokrates_image
        self.workspace_dir = os.path.join(os.getcwd(), 'zokrates')
        
    def compile_zokrates_program(self, program_file: str) -> Dict:
        """
        ZoKrates 프로그램을 컴파일합니다.
        
        Args:
            program_file: 컴파일할 .zok 파일 경로
            
        Returns:
            컴파일 결과 정보
        """
        try:
            # ZoKrates 프로그램이 존재하는지 확인
            program_path = os.path.join(self.workspace_dir, program_file)
            if not os.path.exists(program_path):
                raise FileNotFoundError(f"ZoKrates program not found: {program_path}")
            
            # Docker를 사용하여 ZoKrates 컴파일 실행
            cmd = [
                'docker', 'run', '--rm', '-v',
                f'{self.workspace_dir}:/home/zokrates/code',
                '-w', '/home/zokrates/code',
                self.zokrates_image,
                'zokrates', 'compile', '-i', program_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'message': 'ZoKrates program compiled successfully',
                    'output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'message': 'ZoKrates compilation failed',
                    'error': result.stderr
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Compilation error: {str(e)}',
                'error': str(e)
            }
    
    def setup_zokrates_program(self, program_file: str) -> Dict:
        """
        ZoKrates 프로그램의 setup을 실행합니다.
        
        Args:
            program_file: .zok 파일명 (확장자 제외)
            
        Returns:
            Setup 결과 정보
        """
        try:
            cmd = [
                'docker', 'run', '--rm', '-v',
                f'{self.workspace_dir}:/home/zokrates/code',
                '-w', '/home/zokrates/code',
                self.zokrates_image,
                'zokrates', 'setup', '-i', f'{program_file}.out'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'message': 'ZoKrates setup completed successfully',
                    'output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'message': 'ZoKrates setup failed',
                    'error': result.stderr
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Setup error: {str(e)}',
                'error': str(e)
            }
    
    def compute_witness(self, program_file: str, inputs: List[str]) -> Dict:
        """
        ZoKrates 프로그램의 witness를 계산합니다.
        
        Args:
            program_file: .zok 파일명 (확장자 제외)
            inputs: 프로그램 입력값들
            
        Returns:
            Witness 계산 결과
        """
        try:
            cmd = [
                'docker', 'run', '--rm', '-v',
                f'{self.workspace_dir}:/home/zokrates/code',
                '-w', '/home/zokrates/code',
                self.zokrates_image,
                'zokrates', 'compute-witness', '-i', f'{program_file}.out', '-a'
            ] + inputs
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'message': 'Witness computed successfully',
                    'output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Witness computation failed',
                    'error': result.stderr
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Witness computation error: {str(e)}',
                'error': str(e)
            }
    
    def generate_proof(self, program_file: str) -> Dict:
        """
        ZoKrates 프로그램의 proof를 생성합니다.
        
        Args:
            program_file: .zok 파일명 (확장자 제외)
            
        Returns:
            Proof 생성 결과
        """
        try:
            cmd = [
                'docker', 'run', '--rm', '-v',
                f'{self.workspace_dir}:/home/zokrates/code',
                '-w', '/home/zokrates/code',
                self.zokrates_image,
                'zokrates', 'generate-proof', '-i', f'{program_file}.out'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # proof.json 파일 읽기
                proof_file = os.path.join(self.workspace_dir, 'proof.json')
                if os.path.exists(proof_file):
                    with open(proof_file, 'r') as f:
                        proof_data = json.load(f)
                    
                    return {
                        'status': 'success',
                        'message': 'Proof generated successfully',
                        'proof': proof_data
                    }
                else:
                    return {
                        'status': 'error',
                        'message': 'Proof file not found',
                        'output': result.stdout
                    }
            else:
                return {
                    'status': 'error',
                    'message': 'Proof generation failed',
                    'error': result.stderr
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Proof generation error: {str(e)}',
                'error': str(e)
            }
    
    def verify_proof(self, program_file: str) -> Dict:
        """
        ZoKrates 프로그램의 proof를 검증합니다.
        
        Args:
            program_file: .zok 파일명 (확장자 제외)
            
        Returns:
            Proof 검증 결과
        """
        try:
            cmd = [
                'docker', 'run', '--rm', '-v',
                f'{self.workspace_dir}:/home/zokrates/code',
                '-w', '/home/zokrates/code',
                self.zokrates_image,
                'zokrates', 'verify', '-i', f'{program_file}.out'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'message': 'Proof verified successfully',
                    'output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Proof verification failed',
                    'error': result.stderr
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Proof verification error: {str(e)}',
                'error': str(e)
            }
    
    def create_credit_score_proof(self, credit_score: int, credit_grade: str, 
                                 max_loan_amount: int) -> Dict:
        """
        신용등급 정보를 기반으로 ZK-Proof를 생성합니다.
        
        Args:
            credit_score: 신용점수
            credit_grade: 신용등급
            max_loan_amount: 최대 대출 가능 금액
            
        Returns:
            ZK-Proof 생성 결과
        """
        try:
            # Mock ZK-Proof 생성 (실제로는 ZoKrates를 사용)
            proof_data = {
                'proof_id': f'PROOF_{int(time.time() * 1000000)}_{str(uuid.uuid4())[:8]}',
                'credit_score_hash': hashlib.sha256(str(credit_score).encode()).hexdigest(),
                'credit_grade_hash': hashlib.sha256(credit_grade.encode()).hexdigest(),
                'max_loan_amount_hash': hashlib.sha256(str(max_loan_amount).encode()).hexdigest(),
                'proof_timestamp': datetime.now().isoformat(),
                'zk_proof': {
                    'a': ['0x1234567890abcdef', '0xabcdef1234567890'],
                    'b': [['0x1111111111111111', '0x2222222222222222'], 
                          ['0x3333333333333333', '0x4444444444444444']],
                    'c': ['0x5555555555555555', '0x6666666666666666']
                },
                'public_inputs': [
                    hashlib.sha256(str(credit_score).encode()).hexdigest(),
                    hashlib.sha256(credit_grade.encode()).hexdigest(),
                    hashlib.sha256(str(max_loan_amount).encode()).hexdigest()
                ]
            }
            
            return {
                'status': 'success',
                'message': 'Credit score ZK-Proof generated successfully',
                'proof_data': proof_data
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Credit score proof generation error: {str(e)}',
                'error': str(e)
            }
    
    def verify_credit_score_proof(self, proof_data: Dict) -> Dict:
        """
        신용등급 ZK-Proof를 검증합니다.
        
        Args:
            proof_data: 검증할 proof 데이터
            
        Returns:
            Proof 검증 결과
        """
        try:
            # Mock 검증 (실제로는 ZoKrates를 사용)
            if 'zk_proof' in proof_data and 'public_inputs' in proof_data:
                # 간단한 검증 로직
                is_valid = (
                    len(proof_data['zk_proof']['a']) == 2 and
                    len(proof_data['zk_proof']['b']) == 2 and
                    len(proof_data['zk_proof']['c']) == 2 and
                    len(proof_data['public_inputs']) == 3
                )
                
                if is_valid:
                    return {
                        'status': 'success',
                        'message': 'Credit score proof verified successfully',
                        'is_valid': True
                    }
                else:
                    return {
                        'status': 'error',
                        'message': 'Credit score proof verification failed',
                        'is_valid': False
                    }
            else:
                return {
                    'status': 'error',
                    'message': 'Invalid proof data structure',
                    'is_valid': False
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Proof verification error: {str(e)}',
                'is_valid': False,
                'error': str(e)
            }

# 전역 ZKP 유틸리티 인스턴스
zkp_utils = ZKPUtils() 