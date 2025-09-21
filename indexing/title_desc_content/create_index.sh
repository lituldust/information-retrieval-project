#!/bin/bash
# Bash script to create Lucene index using Pyserini

echo "Creating Lucene index..."
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input . \
  --index ../indexes/title_desc_content_jsonl \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw

if [ $? -eq 0 ]; then
    echo "Indexing completed successfully!"
else
    echo "Error: Indexing failed!"
    exit 1
fi