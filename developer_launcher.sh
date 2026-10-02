#!/bin/bash

clear

echo "========================================="
echo "        🔥 SafeSpace AI Launcher"
echo "========================================="
echo ""

echo "1. Check Project Status"

echo "2. Test Retriever"

echo "3. Test Context Builder"

echo "4. Test Prompt Builder"

echo "5. Test AI Generator"

echo "6. Start SafeSpace AI Chat"

echo "7. Rebuild Chunks"

echo "8. Rebuild Embeddings"

echo "9. Exit"

echo ""

read -p "Choose an option: " choice

cd ~/Desktop/SafeSpace_AI/rag_implement

case $choice in

1)

python check_db.py

;;

2)

python test_retriever.py

;;

3)

python test_context_builder.py

;;

4)

python test_prompt_builder.py

;;

5)

python test_generator.py

;;

6)

python chat.py

;;

7)

python chunk_loader.py

;;

8)

rm -rf vector_db

python embedding_generator.py

;;

9)

echo "Goodbye 👋"

exit

;;

*)

echo "Invalid Choice"

;;

esac