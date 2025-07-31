# 🏦 ZK-NFT 신용대출 시스템

Zero-Knowledge Proof와 NFT를 활용한 프라이버시 보존 신용대출 시스템

## 📋 목차
- [개요](#개요)
- [핵심 기능](#핵심-기능)
- [시스템 아키텍처](#시스템-아키텍처)
- [설치 및 실행](#설치-및-실행)
- [API 문서](#api-문서)
- [테스트](#테스트)
- [데모](#데모)
- [프로젝트 구조](#프로젝트-구조)

## 🎯 개요

ZK-NFT 신용대출 시스템은 **Zero-Knowledge Proof (ZKP)**와 **NFT (Non-Fungible Token)**를 활용하여 개인 신용정보를 노출하지 않으면서도 신용등급을 검증할 수 있는 혁신적인 대출 시스템입니다.

### 핵심 가치
- 🔒 **프라이버시 보호**: 개인 신용정보 노출 없이 검증
- 🏛️ **신뢰성**: 블록체인 기반 불변성
- ⚡ **효율성**: NFT 재사용으로 중복 검증 방지
- 📊 **투명성**: 검증 과정의 투명한 기록

## ⚡ 핵심 기능

### 1. Zero-Knowledge Proof
- 신용정보 노출 없이 신용등급 증명
- 수학적 암호화 기반 검증
- 프라이버시 보호 강화

### 2. NFT 기반 신용증명
- 블록체인에 저장되는 신용등급 증명서
- 불변성 및 신뢰성 보장
- 재사용 가능한 디지털 자산

### 3. 스마트 재사용 시스템
- 1개월 유효기간 설정
- 유효기간 내 자동 재사용
- 효율성 및 비용 절감

### 4. 실시간 검증
- 즉시 신용정보 검증
- 실시간 대출 승인/거절
- 투명한 검증 과정

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   고객 (Customer) │    │   은행 (Bank)    │    │ 외부기관 (External) │
│                 │    │                 │    │                 │
│ • 대출 요청      │───▶│ • 요청 검증      │───▶│ • 신용정보 조회   │
│ • NFT 조회       │    │ • 외부기관 연동  │    │ • ZK-Proof 생성  │
│ • 결과 확인      │◀───│ • 승인/거절 결정 │◀───│ • NFT 발행       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   블록체인      │    │   목업 데이터    │
                       │                 │    │                 │
                       │ • NFT 저장      │    │ • 신용정보      │
                       │ • 검증 기록     │    │ • 은행 기준     │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. ZoKrates 설정 (Windows PowerShell)
```powershell
cd zokrates
.\compile.ps1
```

### 3. 서버 실행
```bash
python app.py
```

### 4. 테스트 실행
```bash
python run.py --test
```

## 🔌 API 문서

### 은행 API (`/api/bank/`)

#### 대출 요청
```http
POST /api/bank/loan-request
Content-Type: application/json

{
    "customer_id": "CUST_001",
    "customer_name": "김철수",
    "requested_amount": 15000000,
    "purpose": "사업자금",
    "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
}
```

#### NFT 검증
```http
POST /api/bank/verify-nft
Content-Type: application/json

{
    "token_id": "NFT_PROOF_INQ_CUST_001_1753980529_1753980529",
    "customer_id": "CUST_001"
}
```

### 외부기관 API (`/api/external/`)

#### 신용정보 조회
```http
POST /api/external/credit-inquiry
Content-Type: application/json

{
    "customer_id": "CUST_001",
    "customer_name": "김철수",
    "requested_amount": 15000000,
    "purpose": "사업자금",
    "request_id": "REQ_CUST_001_1753980529",
    "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
}
```

#### NFT 조회
```http
POST /api/external/my-nft
Content-Type: application/json

{
    "customer_id": "CUST_001",
    "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
}
```

#### ZK-Proof 생성
```http
POST /api/external/generate-proof
Content-Type: application/json

{
    "customer_id": "CUST_001",
    "credit_score": 750,
    "credit_grade": "B",
    "max_loan_amount": 50000000
}
```

#### NFT 발행
```http
POST /api/external/mint-nft
Content-Type: application/json

{
    "proof_id": "PROOF_TEST_001",
    "customer_id": "CUST_001",
    "credit_grade": "B",
    "max_loan_amount": 50000000,
    "customer_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
}
```

## 🧪 테스트

### 종합 테스트 실행
```bash
python tests/test_comprehensive.py
```

## 🎤 데모

### 발표용 데모 실행
```bash
python demo_presentation.py
```

데모 시나리오:
1. **신규 고객 대출 신청**: NFT 생성 및 발행
2. **NFT 재사용**: 효율성 증대 시연
3. **다양한 신용등급**: A, B, C등급 고객 처리
4. **대출 거절 케이스**: 한도 초과 시나리오
5. **ZK-Proof 검증**: 프라이버시 보호 시연

## 📁 프로젝트 구조

```
zk-nft/
├── api/                    # API 엔드포인트
│   ├── __init__.py
│   ├── bank.py            # 은행 관련 API
│   ├── customer.py        # 고객 관련 API
│   └── external.py        # 외부기관 관련 API
├── blockchain/            # 블록체인 관련
│   ├── contracts/         # 스마트 컨트랙트
│   └── package.json
├── data/                  # 목업 데이터
│   ├── bank_criteria.json # 은행 기준 데이터
│   └── credit_data.json   # 신용정보 데이터
├── tests/                 # 테스트 파일
│   ├── test_simple.py     # 기본 API 테스트
│   ├── test_zkp.py        # ZK-Proof 테스트
│   └── test_comprehensive.py # 종합 테스트
├── utils/                 # 유틸리티
│   ├── __init__.py
│   ├── blockchain_utils.py # 블록체인 유틸
│   └── zkp_utils.py       # ZK-Proof 유틸
├── zokrates/              # ZoKrates 관련
│   ├── credit_score.zok   # 신용점수 계산 프로그램
│   ├── compile.ps1        # Windows 컴파일 스크립트
│   └── out/               # 컴파일 결과물
├── app.py                 # 메인 애플리케이션
├── run.py                 # 실행 스크립트
├── requirements.txt       # Python 의존성
├── demo_presentation.py   # 발표용 데모
├── SYSTEM_OVERVIEW.md     # 시스템 전체 개요
└── README.md             # 프로젝트 문서
```

## 🎯 사용자 플로우

### Phase 1: 대출 요청 및 NFT 생성
1. 고객이 은행에 대출 요청
2. 은행이 외부기관에 신용정보 조회 요청
3. 외부기관이 신용정보 조회 및 ZK-Proof 생성
4. NFT 발행 및 블록체인 저장
5. 은행이 최종 승인/거절 결정
6. 고객에게 결과 및 NFT 정보 전달

### Phase 2: NFT 재사용 (유효기간 내)
1. 동일 고객이 추가 대출 요청
2. 기존 NFT 확인 및 유효성 검증
3. NFT에서 신용정보 추출
4. 신용정보 조회 생략, 즉시 승인/거절
5. 고객에게 결과 전달

### Phase 3: NFT 관리
1. 고객이 자신의 NFT 조회
2. 유효기간 확인
3. NFT 상태 및 속성 정보 제공

## 🔒 보안 및 프라이버시

### Zero-Knowledge Proof
- 신용정보 노출 없이 신용등급 증명
- 수학적 암호화 기반 검증
- 프라이버시 보호 강화

### 블록체인 보안
- 분산 저장으로 보안 강화
- 조작 불가능한 기록
- 감사 추적 가능

### NFT 유효성 관리
- 1개월 자동 만료 시스템
- 유효기간 내 재사용
- 만료 시 자동 갱신

## 🚀 향후 발전 방향

### 1. 확장성
- 다중 은행 지원
- 다양한 신용정보 제공업체 연동
- 국제 표준 준수

### 2. 기능 강화
- 실시간 신용정보 업데이트
- AI 기반 신용평가
- 크로스체인 호환성

### 3. 사용자 경험
- 모바일 앱 개발
- 직관적인 UI/UX
- 다국어 지원

## 🔗 블록체인 연동 (추후 진행)

### 현재 상태
- **Mock 기반 구현**: 실제 블록체인 연결 없이 Mock 데이터로 동작
- **개발 편의성**: ganache-cli 없이도 개발/테스트 가능
- **PoC 단계**: 개념 증명에는 현재 상태로 충분

### 실제 블록체인 연동 계획

#### 1. 로컬 블록체인 설정
```bash
# ganache-cli 설치
npm install -g ganache-cli

# 로컬 블록체인 실행
ganache-cli --port 8545 --networkId 1337 --accounts 10 --deterministic

# 또는 Docker 사용
docker run -d --name ganache -p 8545:8545 trufflesuite/ganache-cli:latest
```

#### 2. 스마트 컨트랙트 배포
```bash
# 블록체인 디렉토리로 이동
cd blockchain

# 의존성 설치
npm install

# 컨트랙트 컴파일 및 배포
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

#### 3. 환경 설정 업데이트
```bash
# .env 파일에 실제 컨트랙트 주소 추가
BLOCKCHAIN_URL=http://localhost:8545
CONTRACT_ADDRESS=0x...  # 배포된 컨트랙트 주소
PRIVATE_KEY=0x...       # 배포자 개인키
```

#### 4. Mock → 실제 블록체인 교체
- `utils/blockchain_utils.py`의 Mock 함수들을 실제 Web3 호출로 교체
- `api/external.py`의 NFT 발행 로직을 실제 블록체인 연동으로 변경
- 가스비 및 트랜잭션 관리 로직 추가

#### 5. 테스트 환경 구성
```bash
# 블록체인 연동 테스트
python tests/test_blockchain.py

# 전체 시스템 테스트 (블록체인 포함)
python tests/test_comprehensive_with_blockchain.py
```

### 장점
- **실제 블록체인 환경**: 진짜 NFT 발행 및 검증
- **완전한 분산화**: 중앙화된 서버 의존성 제거
- **투명성**: 모든 거래가 블록체인에 기록
- **불변성**: 조작 불가능한 신용정보 기록

### 고려사항
- **가스비**: 이더리움 네트워크 사용 시 가스비 발생
- **확장성**: 블록체인 처리 속도 제한
- **복잡성**: 계정 관리, 개인키 보안 등 추가 고려사항
- **규제**: 블록체인 기반 금융 서비스 관련 규제 준수

## 🔧 추후 보강 사항

### 현재 Mock 구현 현황

현재 프로젝트는 **Proof of Concept (PoC)** 단계로, 대부분의 핵심 기능이 Mock으로 구현되어 있습니다. 실제 서비스로 발전시키기 위해서는 다음 부분들을 실제 구현으로 교체해야 합니다.

#### 1. 블록체인 연동
**현재 상태:**
- ✅ Mock NFT 발행 (`utils/blockchain_utils.py`)
- ✅ 가짜 트랜잭션 해시 생성
- ✅ 메모리 기반 NFT 저장소

**보강 필요:**
- ❌ 실제 Web3 호출 및 스마트 컨트랙트 함수 실행
- ❌ ganache-cli 또는 실제 이더리움 네트워크 연동
- ❌ 가스비 및 트랜잭션 관리
- ❌ 계정 및 개인키 보안 관리

#### 2. Zero-Knowledge Proof
**현재 상태:**
- ✅ Mock ZK-Proof 생성 (`utils/zkp_utils.py`)
- ✅ 가짜 proof 데이터 구조
- ✅ 간단한 Mock 검증 로직

**보강 필요:**
- ❌ 실제 ZoKrates 컴파일 및 실행
- ❌ 수학적 암호화 기반 proof 생성
- ❌ 실제 ZK-Proof 검증 알고리즘
- ❌ proof 데이터의 암호학적 보안

#### 3. 데이터베이스 연동
**현재 상태:**
- ✅ Mock 신용정보 (`data/credit_data.json`)
- ✅ Mock 은행 기준 (`data/bank_criteria.json`)
- ✅ 메모리 기반 NFT 저장소

**보강 필요:**
- ❌ 실제 데이터베이스 (PostgreSQL, MongoDB 등)
- ❌ 실제 신용정보 제공업체 API 연동
- ❌ 실시간 데이터 동기화
- ❌ 데이터 백업 및 복구 시스템

#### 4. API 엔드포인트
**현재 상태:**
- ✅ Mock 응답 반환 (`api/bank.py`, `api/external.py`, `api/customer.py`)
- ✅ 가짜 데이터 처리
- ✅ 기본적인 HTTP 응답

**보강 필요:**
- ❌ 실제 비즈니스 로직 구현
- ❌ 에러 처리 및 로깅 강화
- ❌ API 인증 및 권한 관리
- ❌ 요청/응답 검증 및 보안

#### 5. 신용정보 시스템
**현재 상태:**
- ✅ Mock 신용정보 조회
- ✅ 고정된 신용점수 및 등급
- ✅ 단순한 대출 한도 계산

**보강 필요:**
- ❌ 실제 신용정보 제공업체 연동
- ❌ 실시간 신용정보 업데이트
- ❌ 복잡한 신용평가 알고리즘
- ❌ 신용정보 보안 및 암호화

### 보강 우선순위

#### Phase 1: 핵심 기능 (높은 우선순위)
1. **실제 블록체인 연동**
   - ganache-cli 설정
   - 스마트 컨트랙트 배포
   - Web3 호출 구현

2. **실제 ZK-Proof 생성**
   - ZoKrates 환경 구축
   - 실제 proof 생성 로직
   - 검증 알고리즘 구현

#### Phase 2: 데이터 관리 (중간 우선순위)
3. **데이터베이스 연동**
   - DB 스키마 설계
   - ORM 설정
   - 데이터 마이그레이션

4. **신용정보 시스템**
   - 신용정보 제공업체 API 연동
   - 실시간 데이터 처리
   - 보안 강화

#### Phase 3: 시스템 안정성 (낮은 우선순위)
5. **API 보안 강화**
   - 인증/인가 시스템
   - API 게이트웨이
   - 모니터링 및 로깅

6. **성능 최적화**
   - 캐싱 시스템
   - 로드 밸런싱
   - 확장성 개선

### 기술 스택 권장사항

#### 블록체인
- **개발 환경**: ganache-cli, Hardhat
- **스마트 컨트랙트**: Solidity, OpenZeppelin
- **Web3 라이브러리**: web3.py, ethers.js

#### 데이터베이스
- **주 데이터베이스**: PostgreSQL
- **캐시**: Redis
- **ORM**: SQLAlchemy

#### ZK-Proof
- **프레임워크**: ZoKrates, Circom
- **검증**: snarkjs, libsnark

#### API 보안
- **인증**: JWT, OAuth 2.0
- **암호화**: AES, RSA
- **API 게이트웨이**: Kong, AWS API Gateway

### 개발 가이드

각 보강 사항에 대한 상세한 구현 가이드는 별도 문서로 제공될 예정입니다:
- `docs/blockchain-integration.md`
- `docs/zkp-implementation.md`
- `docs/database-setup.md`
- `docs/api-security.md`

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

*이 프로젝트는 ZK-NFT 기술을 활용한 혁신적인 신용대출 시스템의 Proof-of-Concept입니다.*