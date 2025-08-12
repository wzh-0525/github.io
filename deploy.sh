#!/bin/bash

# 部署脚本 - 将查询网格分析工具部署到GitHub Pages

# 设置变量
REPO_NAME="github.io"
GITHUB_USER="wzh-0525"  # 已设置为您提供的用户名

# 检查必要依赖
echo "检查系统依赖..."
command -v git >/dev/null 2>&1 || { echo >&2 "需要安装Git"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo >&2 "需要安装cURL"; exit 1; }
command -v jq >/dev/null 2>&1 || { 
    echo "需要安装jq，正在尝试安装..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install jq
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install -y jq
    else
        echo "无法自动安装jq，请手动安装"
        exit 1
    fi
}

# 获取GitHub访问令牌
read -s -p "请输入您的GitHub访问令牌: " GITHUB_TOKEN
echo

# 1. 初始化本地Git仓库
echo "初始化Git仓库..."
git init
git add .
git commit -m "部署查询网格分析工具"

# 仓库已存在，跳过创建步骤
echo "使用现有仓库: $REPO_NAME..."

# 3. 添加远程仓库
echo "配置远程仓库..."
git remote add origin git@github.com:$GITHUB_USER/$REPO_NAME.git

# 4. 推送到GitHub
echo "推送代码到GitHub..."
git push -f -u origin main

# 5. 启用GitHub Pages
echo "启用GitHub Pages..."
curl -H "Authorization: token $GITHUB_TOKEN" \
     -X POST -H "Accept: application/vnd.github+json" \
     -H "Content-Type: application/json" \
     -d '{"source":{"branch":"main","path":"/"}}' \
     https://api.github.com/repos/$GITHUB_USER/$REPO_NAME/pages

# 6. 获取部署URL
echo "获取部署URL..."
sleep 20  # 延长等待时间确保部署完成
DEPLOY_URL=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                  https://api.github.com/repos/$GITHUB_USER/$REPO_NAME/pages | jq -r '.html_url')

# 7. 输出结果
echo -e "\n\033[32m部署成功！\033[0m"
echo "您的查询网格分析工具已部署到:"
echo -e "\033[34m$DEPLOY_URL\033[0m"
echo "请将上面的链接分享给同事使用"
