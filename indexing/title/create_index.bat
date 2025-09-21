@echo off
REM Batch script to create Lucene index using Pyserini

echo Creating Lucene index...
python -m pyserini.index.lucene ^
  --collection JsonCollection ^
  --input . ^
  --index ../indexes/title_jsonl ^
  --generator DefaultLuceneDocumentGenerator ^
  --threads 1 ^
  --storePositions --storeDocvectors --storeRaw

if %errorlevel% neq 0 (
    echo Error: Indexing failed!
    pause
    exit /b %errorlevel%
) else (
    echo Indexing completed successfully!
    pause
)