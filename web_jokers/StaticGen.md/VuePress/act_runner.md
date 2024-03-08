---
layout: default
title: act_runner
parent: VuePress
grand_parent: Static Site Generators
nav_order: 1
last_modified_date: 2024-03-08 17:02:20
tags: VuPress
---

# act_runner settings
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景

## docker-compose.yml

```yml
kuang@eng06 /nas2/VuePress
$ cat docker-compose.yml
version: "3"

services:
  runner:
    image: gitea/act_runner:0.2.6
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /workspace/GiteaTeam/VuePress:/app
      - .:/app
    working_dir: /app
    environment:
      - GITEA_INSTANCE_URL=http://eng06.sinotech-eng.com:3000/
      - GITEA_RUNNER_REGISTRATION_TOKEN=***
```

## main.yml

```yml
name: CI
on: [push]
jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - uses: pnpm/action-setup@v2
        with:
          version: 7            
      - uses: actions/checkout@v4
      - name: build vuepress
        run: |
          cd $GITHUB_WORKSPACE
          pnpm install --no-frozen-lockfile && pnpm run docs:build
      - name: Copy files via scp
        run: |
          ls -lh ${GITHUB_WORKSPACE}/src/.vuepress/dist/*
      - name: Update remote SSH configs  
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          password: ${{ secrets.SERVER_PASS }}
          script: |
            mkdir -p ~/.ssh
            cat > ~/.ssh/config << EOF
            Host *
              KexAlgorithms +diffie-hellman-group1-sha1
              Ciphers +aes256-cbc,aes192-cbc,aes128-cbc
              MACs +umac-64@openssh.com
            EOF
      - name: scp dist
        run: |
          export host=${{ secrets.SERVER_HOST }}
          export user=${{ secrets.SERVER_USER }}
          export pass=${{ secrets.SERVER_PASS }}
          export local_path='/workspace/GiteaTeam/VuePress/src/.vuepress/dist/*'
          export target='/nas2/VuePressDist'
          apt-get update
          apt-get install -y sshpass
          mkdir -p ~/.ssh
          cat > ~/.ssh/config << EOF
          Host *
            KexAlgorithms +diffie-hellman-group1-sha1
            Ciphers +aes256-cbc,aes192-cbc,aes128-cbc
            MACs +umac-64@openssh.com
          EOF
          sshpass -p ${pass} scp -v -r -F ~/.ssh/config -o 'StrictHostKeyChecking no' ${local_path} ${user}@${host}:${target}
```