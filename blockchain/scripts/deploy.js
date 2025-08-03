const hre = require("hardhat");

async function main() {
  console.log("🚀 Starting CreditGradeNFT contract deployment...");

  // 배포자 계정 가져오기
  const [deployer] = await ethers.getSigners();
  console.log("📝 Deploying contracts with account:", deployer.address);

  // 계정 잔액 확인
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("💰 Account balance:", ethers.formatEther(balance), "ETH");

  // CreditGradeNFT 컨트랙트 배포
  const CreditGradeNFT = await hre.ethers.getContractFactory("CreditGradeNFT");
  const creditGradeNFT = await CreditGradeNFT.deploy(
    "Credit Grade NFT",  // 컬렉션 이름
    "CGNFT"              // 컬렉션 심볼
  );

  await creditGradeNFT.waitForDeployment();
  const contractAddress = await creditGradeNFT.getAddress();

  console.log("✅ CreditGradeNFT deployed to:", contractAddress);

  // 배포 정보 출력
  console.log("\n📋 Deployment Summary:");
  console.log("Contract Name: CreditGradeNFT");
  console.log("Contract Address:", contractAddress);
  console.log("Deployer Address:", deployer.address);
  console.log("Network:", hre.network.name);

  // 컨트랙트 정보 저장
  const deploymentInfo = {
    contractName: "CreditGradeNFT",
    contractAddress: contractAddress,
    deployerAddress: deployer.address,
    network: hre.network.name,
    deploymentTime: new Date().toISOString(),
    constructorArgs: {
      name: "Credit Grade NFT",
      symbol: "CGNFT"
    }
  };

  // 배포 정보를 파일로 저장
  const fs = require('fs');
  const path = require('path');
  
  const deploymentPath = path.join(__dirname, '../deployment.json');
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  
  console.log("💾 Deployment info saved to:", deploymentPath);

  // 환경 변수 파일 생성 (Python에서 사용)
  const envContent = `# Blockchain Configuration
BLOCKCHAIN_URL=http://localhost:8545
CONTRACT_ADDRESS=${contractAddress}
DEPLOYER_ADDRESS=${deployer.address}
NETWORK_ID=1337

# Contract Information
CONTRACT_NAME=CreditGradeNFT
CONTRACT_SYMBOL=CGNFT
`;
  
  const envPath = path.join(__dirname, '../../.env');
  fs.writeFileSync(envPath, envContent);
  
  console.log("🔧 Environment file created:", envPath);

  console.log("\n🎉 Deployment completed successfully!");
  console.log("Next steps:");
  console.log("1. Start your Python application");
  console.log("2. The contract address will be automatically loaded from .env file");
  console.log("3. Test the blockchain integration");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  }); 