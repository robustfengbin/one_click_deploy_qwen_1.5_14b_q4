#!/bin/bash
# 安装vim
sudo apt-get update
sudo apt-get install -y vim
## 安装ollama
curl -fsSL https://ollama.com/install.sh | sh
nohup ollama serve > ollama_server_log.txt 2>&1 &
ollama run qwen:14b-chat-q4_K_S


