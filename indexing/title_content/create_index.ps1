# PowerShell script to create Lucene index using Pyserini

Write-Host "Creating Lucene index..." -ForegroundColor Green

try {
    & python -m pyserini.index.lucene `
      --collection JsonCollection `
      --input . `
      --index ../indexes/title_content_jsonl `
      --generator DefaultLuceneDocumentGenerator `
      --threads 1 `
      --storePositions --storeDocvectors --storeRaw
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Indexing completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Error: Indexing failed!" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "Error running indexing command: $_" -ForegroundColor Red
    exit 1
}

# Pause to see output
Read-Host "Press Enter to continue..."