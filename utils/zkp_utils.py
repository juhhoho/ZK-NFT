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
    
    def __init__(self, zokrates_image: str = "zokrates/zokrates:latest"):
        """
        ZKP 유틸리티 초기화
        
        Args:
            zokrates_image: ZoKrates Docker 이미지명
        """
        self.zokrates_image = zokrates_image
        
        # 현재 작업 디렉토리에서 zokrates 폴더를 찾기
        current_dir = os.getcwd()
        zokrates_dir = os.path.join(current_dir, 'zokrates')
        
        # 만약 현재 디렉토리가 이미 zokrates라면, 상위 디렉토리에서 찾기
        if os.path.basename(current_dir) == 'zokrates':
            zokrates_dir = current_dir
        elif not os.path.exists(zokrates_dir):
            # 상위 디렉토리에서 zokrates 폴더 찾기
            parent_dir = os.path.dirname(current_dir)
            zokrates_dir = os.path.join(parent_dir, 'zokrates')
            
        self.workspace_dir = zokrates_dir
        
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
                'zokrates', 'setup', '-i', 'out'
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
                    'error': f"Command: {' '.join(cmd)}\nReturn code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
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
                'zokrates', 'compute-witness', '-i', 'out', '-a'
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
                'zokrates', 'generate-proof', '-i', 'out'
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
                'zokrates', 'verify'
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
        신용등급 정보를 기반으로 실제 ZoKrates ZK-Proof를 생성합니다.
        
        Args:
            credit_score: 신용점수
            credit_grade: 신용등급 (A, B, C, D, E)
            max_loan_amount: 최대 대출 가능 금액
            
        Returns:
            ZK-Proof 생성 결과
        """
        try:
            # 신용등급을 숫자로 변환 (A=1, B=2, C=3, D=4, E=5)
            grade_mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
            credit_grade_num = grade_mapping.get(credit_grade.upper(), 5)
            
            # ZoKrates 프로그램 컴파일
            compile_result = self.compile_zokrates_program('credit_score.zok')
            if compile_result['status'] != 'success':
                return {
                    'status': 'error',
                    'message': 'ZoKrates compilation failed',
                    'error': compile_result.get('error', 'Unknown compilation error')
                }
            
            # ZoKrates setup 실행
            setup_result = self.setup_zokrates_program('credit_score')
            if setup_result['status'] != 'success':
                return {
                    'status': 'error',
                    'message': 'ZoKrates setup failed',
                    'error': setup_result.get('error', 'Unknown setup error')
                }
            
            # Witness 계산
            inputs = [str(credit_score), str(credit_grade_num), str(max_loan_amount)]
            witness_result = self.compute_witness('credit_score', inputs)
            if witness_result['status'] != 'success':
                return {
                    'status': 'error',
                    'message': 'Witness computation failed',
                    'error': witness_result.get('error', 'Unknown witness error')
                }
            
            # Proof 생성
            proof_result = self.generate_proof('credit_score')
            if proof_result['status'] != 'success':
                return {
                    'status': 'error',
                    'message': 'Proof generation failed',
                    'error': proof_result.get('error', 'Unknown proof generation error')
                }
            
            # Proof 검증
            verify_result = self.verify_proof('credit_score')
            if verify_result['status'] != 'success':
                return {
                    'status': 'error',
                    'message': 'Proof verification failed',
                    'error': verify_result.get('error', 'Unknown verification error')
                }
            
            # 결과 데이터 구성
            proof_data = {
                'proof_id': f'PROOF_{int(time.time() * 1000000)}_{str(uuid.uuid4())[:8]}',
                'credit_score': credit_score,
                'credit_grade': credit_grade,
                'max_loan_amount': max_loan_amount,
                'proof_timestamp': datetime.now().isoformat(),
                'zk_proof': proof_result['proof'],
                'public_inputs': [
                    hashlib.sha256(str(credit_score).encode()).hexdigest(),
                    hashlib.sha256(credit_grade.encode()).hexdigest(),
                    hashlib.sha256(str(max_loan_amount).encode()).hexdigest()
                ],
                'verification_result': verify_result['output']
            }
            
            return {
                'status': 'success',
                'message': 'Credit score ZK-Proof generated successfully using ZoKrates',
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
        신용등급 ZK-Proof를 실제 ZoKrates로 검증합니다.
        
        Args:
            proof_data: 검증할 proof 데이터
            
        Returns:
            Proof 검증 결과
        """
        try:
            # ZoKrates proof 검증 실행
            verify_result = self.verify_proof('credit_score')
            
            if verify_result['status'] == 'success':
                return {
                    'status': 'success',
                    'message': 'Credit score proof verified successfully using ZoKrates',
                    'is_valid': True,
                    'verification_output': verify_result['output']
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Credit score proof verification failed',
                    'is_valid': False,
                    'error': verify_result.get('error', 'Unknown verification error')
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