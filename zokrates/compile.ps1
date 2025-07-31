# Simple ZoKrates Compilation Script (PowerShell)

# Set UTF-8 encoding for proper display of Korean and emojis
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Starting ZoKrates compilation..." -ForegroundColor Green

$currentDir = Get-Location
Write-Host "Current directory: $currentDir" -ForegroundColor Cyan

# Compile credit score ZK-Proof program
Write-Host "Compiling credit_score.zok..." -ForegroundColor Yellow
docker run --rm -v "${currentDir}:/home/zokrates/code" -w /home/zokrates/code zokrates/zokrates:latest zokrates compile -i credit_score.zok

if ($LASTEXITCODE -ne 0) {
    Write-Host "Compilation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Compilation successful!" -ForegroundColor Green

# Setup
Write-Host "Running setup..." -ForegroundColor Yellow
docker run --rm -v "${currentDir}:/home/zokrates/code" -w /home/zokrates/code zokrates/zokrates:latest zokrates setup -i out

if ($LASTEXITCODE -ne 0) {
    Write-Host "Setup failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Setup completed!" -ForegroundColor Green

# Compute witness
Write-Host "Computing witness..." -ForegroundColor Yellow
docker run --rm -v "${currentDir}:/home/zokrates/code" -w /home/zokrates/code zokrates/zokrates:latest zokrates compute-witness -i out -a 750 2 50000000

if ($LASTEXITCODE -ne 0) {
    Write-Host "Witness computation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Witness computation completed!" -ForegroundColor Green

# Generate proof
Write-Host "Generating proof..." -ForegroundColor Yellow
docker run --rm -v "${currentDir}:/home/zokrates/code" -w /home/zokrates/code zokrates/zokrates:latest zokrates generate-proof -i out

if ($LASTEXITCODE -ne 0) {
    Write-Host "Proof generation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Proof generation completed!" -ForegroundColor Green

# Verify proof
Write-Host "Verifying proof..." -ForegroundColor Yellow
docker run --rm -v "${currentDir}:/home/zokrates/code" -w /home/zokrates/code zokrates/zokrates:latest zokrates verify

if ($LASTEXITCODE -ne 0) {
    Write-Host "Proof verification failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Proof verification successful!" -ForegroundColor Green

Write-Host "ZoKrates setup completed!" -ForegroundColor Green
Write-Host "Generated files:" -ForegroundColor Cyan
Get-ChildItem -Path "*.out", "*.json", "*.key", "witness" -ErrorAction SilentlyContinue | ForEach-Object { Write-Host $_.Name -ForegroundColor White } 