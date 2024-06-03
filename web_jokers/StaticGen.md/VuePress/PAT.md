

GitHub Actions Runner 的確需要 Runner Token 來註冊到 GitHub 倉庫，通常這個 Token 需要手動產生並設定。然而，對於某些情況，您可以透過 GitHub Actions 和 Secrets 實現更自動化的設定流程。

GitHub Pages 本身不需要 Runner Token，您可以使用 GitHub Actions 自動部署到 GitHub Pages。但要使用自架的 Runner，仍需要一些手動設定。

自動取得 Runner Token 的思路

雖然無法完全避免手動產生 Token，但可以使用 GitHub Actions Workflow 和 GitHub Secrets 結合起來實現更自動化的 Runner 註冊流程。

1. 產生 GitHub Personal Access Token (PAT) 並儲存為 GitHub Secret:
• 產生一個具有 repo 和 admin:org 權限的 GitHub PAT。
• 將這個 Token 儲存為 GitHub Secrets，假設命名為 PAT_TOKEN。
2. 使用 GitHub Actions Workflow 取得 Runner Token 並啟動自架式 Runner:

建立一個 GitHub Actions Workflow 檔案 .github/workflows/self-hosted-runner.yml：

name: Setup Self-Hosted Runner

on: [push]

jobs:
 setup-runner:
 runs-on: ubuntu-latest

 steps:
 - name: Checkout
 uses: actions/checkout@v2

 - name: Generate Runner Token
 id: generate_token
 run: |
 repo=$GITHUB_REPOSITORY
 pat=${{ secrets.PAT_TOKEN }}
 token=$(curl -s -X POST -H "Authorization: token $pat" https://api.github.com/repos/$repo/actions/runners/registration-token | jq .token --raw-output )
 echo "::set-output name=token::$token"

 - name: Start Self-Hosted Runner
 run: |
 docker run -d --name actions-runner \
 -e RUNNER_REPO_URL="https://github.com/${{ github.repository }}" \
 -e RUNNER_TOKEN="${{ steps.generate_token.outputs.token }}" \
 github-actions-runner:latest

這個 workflow 會在每次 push 時產生一個 Runner Token 並啟動 Docker 容器中的自架式 Runner。

完整的 Dockerfile 和 Entrypoint

確保 Dockerfile 和 entrypoint.sh 能正確處理這些環境變數：

Dockerfile:

FROM ubuntu:20.04

RUN apt-get update && \
 apt-get install -y \
 curl \
 sudo \
 git \
 jq

RUN useradd -m runner && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER runner

WORKDIR /home/runner

RUN curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.285.1/actions-runner-linux-x64-2.285.1.tar.gz && \
 tar xzf actions-runner.tar.gz && \
 rm actions-runner.tar.gz

COPY entrypoint.sh /entrypoint.sh
RUN sudo chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

entrypoint.sh:

#!/bin/bash

if [ -z "$RUNNER_REPO_URL" ] || [ -z "$RUNNER_TOKEN" ]; then
 echo "RUNNER_REPO_URL and RUNNER_TOKEN must be set"
 exit 1
fi

# Ensure the runner is configured
./config.sh --url $RUNNER_REPO_URL --token $RUNNER_TOKEN --name $(hostname) --work _work --unattended --replace

# Run the runner
./run.sh

透過這種方式，您可以減少手動設定 Runner Token 的步驟，實現更自動化的自架 Runner 部署和註冊流程。
