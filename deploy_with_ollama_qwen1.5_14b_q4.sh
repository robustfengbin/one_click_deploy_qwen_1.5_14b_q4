#!/bin/bash
# 安装vim
sudo apt-get update
sudo apt-get install -y vim
# 进入用户目录
cd ~
# 创建 soft 文件夹
mkdir soft
# 进入 soft 文件夹
cd soft
# 下载 Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh
# 以无人值守模式安装 Anaconda
bash Anaconda3-2023.03-1-Linux-x86_64.sh -b
# 初始化 conda
~/anaconda3/bin/conda init
# 使用 `source ~/.bashrc` 使改变在当前 shell 中生效，而不是关闭并重新打开新的 shell
source ~/.bashrc
# 创建名为 qwen1.5_14b_q4 的新 conda 环境，该环境使用 Python 3.10
~/anaconda3/bin/conda create --name qwen1.5_14b_q4 python=3.10 -y
# 激活 qwen1.5_14b_q4 环境
source ~/anaconda3/bin/activate qwen1.5_14b_q4
# 在用户目录下创建或修改 .bash_profile ，添加以下内容：
echo 'if [ -f ~/.bashrc ]; then
          . ~/.bashrc
  fi
  PATH=$PATH
  export PATH
  conda activate qwen1.5_14b_q4' >> ~/.bash_profile
# 让新的 .bash_profile 生效
source ~/.bash_profile
# 创建 prj 文件夹
mkdir ~/prj

# 进入 prj 文件夹
cd ~/prj
pip3 install torch torchvision torchaudio 
mkdir qwen_1.5_14b_q4
cd qwen_1.5_14b_q4
## 安装ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama run qwen:14b-chat-q4_K_S



