#!/usr/bin/env python3
"""
블록체인 환경 설정 및 컨트랙트 배포 스크립트
Hardhat 로컬 블록체인을 시작하고 컨트랙트를 배포합니다.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """명령어를 실행하고 결과를 반환합니다."""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_node_installed():
    """Node.js가 설치되어 있는지 확인합니다."""
    print("🔍 Checking Node.js installation...")
    node_version = run_command("node --version")
    npm_version = run_command("npm --version")
    
    if node_version and npm_version:
        print(f"✅ Node.js version: {node_version}")
        print(f"✅ npm version: {npm_version}")
        return True
    else:
        print("❌ Node.js or npm not found. Please install Node.js first.")
        return False

def install_dependencies():
    """블록체인 의존성을 설치합니다."""
    print("\n📦 Installing blockchain dependencies...")
    
    blockchain_dir = Path("blockchain")
    if not blockchain_dir.exists():
        print("❌ blockchain directory not found.")
        return False
    
    # npm install 실행
    result = run_command("npm install", cwd=blockchain_dir)
    if result is not None:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False

def start_hardhat_node():
    """Hardhat 로컬 블록체인을 시작합니다."""
    print("\n🚀 Starting Hardhat local blockchain...")
    
    blockchain_dir = Path("blockchain")
    
    # 백그라운드에서 Hardhat 노드 시작
    try:
        process = subprocess.Popen(
            "npx hardhat node",
            cwd=blockchain_dir,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 노드가 시작될 때까지 대기
        time.sleep(5)
        
        # 프로세스가 여전히 실행 중인지 확인
        if process.poll() is None:
            print("✅ Hardhat node started successfully")
            print("   Local blockchain running on http://localhost:8545")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start Hardhat node: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Hardhat node: {e}")
        return None

def deploy_contract():
    """컨트랙트를 배포합니다."""
    print("\n📋 Deploying CreditGradeNFT contract...")
    
    blockchain_dir = Path("blockchain")
    
    # 컨트랙트 컴파일
    print("   Compiling contracts...")
    compile_result = run_command("npx hardhat compile", cwd=blockchain_dir)
    if compile_result is None:
        print("❌ Contract compilation failed")
        return False
    
    print("✅ Contracts compiled successfully")
    
    # 컨트랙트 배포
    print("   Deploying contract...")
    deploy_result = run_command("npx hardhat run scripts/deploy.js --network localhost", cwd=blockchain_dir)
    if deploy_result is None:
        print("❌ Contract deployment failed")
        return False
    
    print("✅ Contract deployed successfully")
    return True

def verify_setup():
    """설정이 올바르게 완료되었는지 확인합니다."""
    print("\n🔍 Verifying blockchain setup...")
    
    # .env 파일 확인
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Environment file (.env) created")
        
        # .env 파일 내용 확인
        with open(env_file, 'r') as f:
            env_content = f.read()
            if "CONTRACT_ADDRESS" in env_content:
                print("✅ Contract address configured")
            else:
                print("❌ Contract address not found in .env")
                return False
    else:
        print("❌ Environment file (.env) not found")
        return False
    
    # deployment.json 파일 확인
    deployment_file = Path("blockchain/deployment.json")
    if deployment_file.exists():
        print("✅ Deployment info file created")
        
        # 배포 정보 확인
        with open(deployment_file, 'r') as f:
            deployment_info = json.load(f)
            print(f"   Contract Address: {deployment_info.get('contractAddress', 'Not found')}")
            print(f"   Deployer Address: {deployment_info.get('deployerAddress', 'Not found')}")
    else:
        print("❌ Deployment info file not found")
        return False
    
    return True

def main():
    """메인 설정 함수"""
    print("🏗️  Blockchain Environment Setup")
    print("=" * 50)
    
    # 1. Node.js 설치 확인
    if not check_node_installed():
        print("\n📋 Please install Node.js from https://nodejs.org/")
        return False
    
    # 2. 의존성 설치
    if not install_dependencies():
        return False
    
    # 3. Hardhat 노드 시작
    node_process = start_hardhat_node()
    if node_process is None:
        return False
    
    try:
        # 4. 컨트랙트 배포
        if not deploy_contract():
            return False
        
        # 5. 설정 확인
        if not verify_setup():
            return False
        
        print("\n" + "=" * 50)
        print("🎉 Blockchain environment setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. The Hardhat node is running in the background")
        print("2. Contract has been deployed and configured")
        print("3. You can now run your Python application")
        print("4. Test the integration with: python tests/test_blockchain_integration.py")
        print("\n⚠️  Note: Keep the Hardhat node running while testing")
        print("   To stop the node, use Ctrl+C in the terminal where it's running")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        return False
    finally:
        # 노드 프로세스 정리
        if node_process:
            node_process.terminate()
            print("\n🛑 Hardhat node stopped")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 