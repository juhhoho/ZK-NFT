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

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

*이 프로젝트는 ZK-NFT 기술을 활용한 혁신적인 신용대출 시스템의 Proof-of-Concept입니다.*