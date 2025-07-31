#!/usr/bin/env python3
"""
zk-nft 프로젝트 실행 스크립트
개발 및 테스트 환경에서 프로젝트를 쉽게 실행할 수 있습니다.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """필요한 의존성들이 설치되어 있는지 확인합니다."""
    print("🔍 의존성 확인 중...")
    
    # Python 버전 확인
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        return False
    
    # 필요한 Python 패키지 확인
    required_packages = [
        'flask', 'flask_cors', 'flask_restful', 'web3', 
        'requests', 'dotenv', 'cryptography'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 다음 패키지들이 설치되지 않았습니다: {', '.join(missing_packages)}")
        print("다음 명령어로 설치하세요:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 모든 의존성이 설치되어 있습니다.")
    return True

def setup_environment():
    """환경 설정을 초기화합니다."""
    print("⚙️ 환경 설정 초기화 중...")
    
    # .env 파일이 없으면 생성
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📝 .env 파일을 생성합니다...")
        with open(env_example, 'r', encoding='utf-8') as f:
            env_content = f.read()
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ .env 파일이 생성되었습니다. 필요에 따라 설정을 수정하세요.")
    
    # 데이터 디렉토리 확인
    data_dir = Path('data')
    if not data_dir.exists():
        print("📁 data 디렉토리를 생성합니다...")
        data_dir.mkdir(exist_ok=True)
    
    print("✅ 환경 설정이 완료되었습니다.")

def run_tests():
    """테스트를 실행합니다."""
    print("🧪 테스트 실행 중...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 모든 테스트가 통과했습니다.")
        else:
            print("❌ 일부 테스트가 실패했습니다.")
            print(result.stdout)
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류가 발생했습니다: {e}")
        return False

def run_server(host='0.0.0.0', port=5000, debug=True):
    """Flask 서버를 실행합니다."""
    print(f"🚀 zk-nft 서버를 시작합니다...")
    print(f"📍 서버 주소: http://{host}:{port}")
    print(f"🔧 디버그 모드: {debug}")
    print("🛑 서버를 중지하려면 Ctrl+C를 누르세요.")
    
    try:
        from app import create_app
        app = create_app()
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 서버가 중지되었습니다.")
    except Exception as e:
        print(f"❌ 서버 실행 중 오류가 발생했습니다: {e}")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='zk-nft 프로젝트 실행 스크립트')
    parser.add_argument('--test', action='store_true', help='테스트 실행')
    parser.add_argument('--setup', action='store_true', help='환경 설정 초기화')
    parser.add_argument('--host', default='0.0.0.0', help='서버 호스트 (기본값: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='서버 포트 (기본값: 5000)')
    parser.add_argument('--no-debug', action='store_true', help='디버그 모드 비활성화')
    
    args = parser.parse_args()
    
    print("🎯 zk-nft 프로젝트 실행 스크립트")
    print("=" * 50)
    
    # 의존성 확인
    if not check_dependencies():
        sys.exit(1)
    
    # 환경 설정
    if args.setup:
        setup_environment()
        return
    
    # 테스트 실행
    if args.test:
        if not run_tests():
            sys.exit(1)
        return
    
    # 기본 환경 설정
    setup_environment()
    
    # 서버 실행
    debug_mode = not args.no_debug
    run_server(args.host, args.port, debug_mode)

if __name__ == '__main__':
    main() 