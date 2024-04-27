#!/bin/bash
# 安装vim
sudo apt-get update
sudo apt-get install -y vim
sudo apt-get install netcat -y
sudo apt-get install net-tools

## 安装ollama
curl -fsSL https://ollama.com/install.sh | sh
nohup ollama serve > ollama_server_log.txt 2>&1 &
nohup ollama serve > ollama_server_log.txt 2>&1 &
while ! netstat -tuln | grep ':11434' > /dev/null; do
  sleep 1 # 每隔1秒检查一次
done

ollama run qwen:14b-chat-q4_K_S


