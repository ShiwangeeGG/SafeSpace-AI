#!/bin/bash

echo "==========================================="
echo "🚀 Starting SafeSpace AI Development Setup"
echo "==========================================="

echo ""

echo "📁 Navigating to Project..."
cd ~/Desktop/SafeSpace_AI

echo "Current Directory:"
pwd

echo ""

echo "🐍 Activating Conda Environment..."
source ~/miniforge3/bin/activate base

echo ""

echo "🤖 Checking Ollama..."

if ollama ps >/dev/null 2>&1
then
    echo "✅ Ollama is running."
else
    echo "⚠️ Ollama is not running."
    echo "Starting Ollama..."
    ollama serve &
    sleep 3
fi

echo ""

echo "📦 Installed Models:"
ollama list

echo ""

echo "📂 Moving to RAG Folder..."
cd rag_implement

echo ""

echo "🗄 Checking Vector Database..."
python check_db.py

echo ""

echo "🎯 SafeSpace AI is Ready!"

echo "==========================================="