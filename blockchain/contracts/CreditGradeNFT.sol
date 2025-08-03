// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title CreditGradeNFT
 * @dev 신용등급을 기반으로 한 NFT 컨트랙트
 * Zero-Knowledge Proof를 통해 검증된 신용등급 정보를 NFT로 발행합니다.
 */
contract CreditGradeNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    
    Counters.Counter private _tokenIds;
    
    // NFT 메타데이터 구조
    struct CreditGradeData {
        string creditGrade;
        uint256 maxLoanAmount;
        string proofId;
        string customerId;
        uint256 issuedAt;
        bool isValid;
    }
    
    // 토큰 ID별 신용등급 데이터 매핑
    mapping(uint256 => CreditGradeData) public creditGradeData;
    
    // 고객별 토큰 ID 매핑
    mapping(string => uint256[]) public customerTokens;
    
    // 발행자 권한 매핑
    mapping(address => bool) public authorizedMinters;
    
    // 이벤트 정의
    event CreditGradeNFTMinted(
        uint256 indexed tokenId,
        string indexed customerId,
        string creditGrade,
        uint256 maxLoanAmount,
        string proofId
    );
    
    event CreditGradeNFTTransferred(
        uint256 indexed tokenId,
        address indexed from,
        address indexed to
    );
    
    event MinterAuthorized(address indexed minter);
    event MinterRevoked(address indexed minter);
    
    /**
     * @dev 컨트랙트 생성자
     * @param name NFT 컬렉션 이름
     * @param symbol NFT 컬렉션 심볼
     */
    constructor(string memory name, string memory symbol) 
        ERC721(name, symbol) 
        Ownable() 
    {
        // 컨트랙트 배포자를 기본 발행자로 설정
        authorizedMinters[msg.sender] = true;
    }
    
    /**
     * @dev 발행자 권한 부여
     * @param minter 발행자 주소
     */
    function authorizeMinter(address minter) external onlyOwner {
        authorizedMinters[minter] = true;
        emit MinterAuthorized(minter);
    }
    
    /**
     * @dev 발행자 권한 해제
     * @param minter 발행자 주소
     */
    function revokeMinter(address minter) external onlyOwner {
        authorizedMinters[minter] = false;
        emit MinterRevoked(minter);
    }
    
    /**
     * @dev 신용등급 NFT 발행
     * @param to NFT 수신자 주소
     * @param tokenURI NFT 메타데이터 URI
     * @param creditGrade 신용등급 (A, B, C, D, E)
     * @param maxLoanAmount 최대 대출 가능 금액
     * @param proofId ZK-Proof ID
     * @param customerId 고객 ID
     */
    function mintCreditGradeNFT(
        address to,
        string memory tokenURI,
        string memory creditGrade,
        uint256 maxLoanAmount,
        string memory proofId,
        string memory customerId
    ) external returns (uint256) {
        require(authorizedMinters[msg.sender], "Not authorized to mint");
        require(to != address(0), "Invalid recipient address");
        require(bytes(creditGrade).length > 0, "Credit grade cannot be empty");
        require(bytes(proofId).length > 0, "Proof ID cannot be empty");
        require(bytes(customerId).length > 0, "Customer ID cannot be empty");
        
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        
        // NFT 발행
        _safeMint(to, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        
        // 신용등급 데이터 저장
        creditGradeData[newTokenId] = CreditGradeData({
            creditGrade: creditGrade,
            maxLoanAmount: maxLoanAmount,
            proofId: proofId,
            customerId: customerId,
            issuedAt: block.timestamp,
            isValid: true
        });
        
        // 고객별 토큰 ID 저장
        customerTokens[customerId].push(newTokenId);
        
        emit CreditGradeNFTMinted(
            newTokenId,
            customerId,
            creditGrade,
            maxLoanAmount,
            proofId
        );
        
        return newTokenId;
    }
    
    /**
     * @dev NFT 전송 (오버라이드)
     */
    function _transfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual override(ERC721) {
        super._transfer(from, to, tokenId);
        
        emit CreditGradeNFTTransferred(tokenId, from, to);
    }
    
    /**
     * @dev 토큰 소멸 (오버라이드)
     */
    function _burn(uint256 tokenId) internal virtual override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
        
        // 신용등급 데이터 무효화
        creditGradeData[tokenId].isValid = false;
    }
    
    /**
     * @dev 토큰 URI 조회 (오버라이드)
     */
    function tokenURI(uint256 tokenId) public view virtual override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }
    
    /**
     * @dev 신용등급 데이터 조회
     * @param tokenId 토큰 ID
     */
    function getCreditGradeData(uint256 tokenId) external view returns (CreditGradeData memory) {
        require(_exists(tokenId), "Token does not exist");
        return creditGradeData[tokenId];
    }
    
    /**
     * @dev 고객의 모든 토큰 ID 조회
     * @param customerId 고객 ID
     */
    function getCustomerTokens(string memory customerId) external view returns (uint256[] memory) {
        return customerTokens[customerId];
    }
    
    /**
     * @dev NFT 유효성 검증
     * @param tokenId 토큰 ID
     */
    function isValidNFT(uint256 tokenId) external view returns (bool) {
        return _exists(tokenId) && creditGradeData[tokenId].isValid;
    }
    
    /**
     * @dev 대출 자격 확인
     * @param tokenId 토큰 ID
     * @param requestedAmount 요청 대출 금액
     */
    function checkLoanEligibility(uint256 tokenId, uint256 requestedAmount) external view returns (bool) {
        require(_exists(tokenId), "Token does not exist");
        require(creditGradeData[tokenId].isValid, "NFT is not valid");
        
        return requestedAmount <= creditGradeData[tokenId].maxLoanAmount;
    }
    
    /**
     * @dev 총 발행된 토큰 수 조회
     */
    function totalSupply() external view returns (uint256) {
        return _tokenIds.current();
    }
    
    /**
     * @dev 컨트랙트 지원 인터페이스 확인 (오버라이드)
     */
    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721, ERC721URIStorage) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
} 