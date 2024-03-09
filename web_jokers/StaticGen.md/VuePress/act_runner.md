---
layout: default
title: gitea CI/CD actions
parent: VuePress
grand_parent: Static Site Generators
nav_order: 1
last_modified_date: 2024-03-09 07:02:20
tags: VuPress
---

# gitea CI/CD actions
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

- Gitea Actions是自動發布的技術核心，是仿照Github Action發展的內部CI/CD工具。有了Actions，外部的CI/CD包括Drone、Jenkins等等都不再需要了。
- Gitea在這個主題發展了很久，直到第19版（目前最新也只21版）才發展這個功能，原因不明，可能也是在觀望大家對Github Page的接受度、技術的穩定度等等因素吧，想來一般人會直覺使用git系統作為後台主軸的必要性並不是很高。
- 總體而言，公司內部倉儲管理的網誌系統的適用性及必要性考量：
  - 更新頻率很快
  - 多人同時協作
  - 內容關乎機敏
  - 不管前端、後端、服務系統，都符合當代最新的環境技術、具發展潛力
- 這些理由寫在上面似乎只是鼓舞自己克服設置過程的困難
  - 因為很新、實例與細節需要發展、測試
  - 會需要docker、虛擬機的觀念對很多人是個障礙
  - Actions使用[YAML](https://zh.wikipedia.org/zh-tw/YAML)語法。
- Actions整體的工作流程圖，可以參考[dev.to這一篇](https://dev.to/efkumah/implementing-cicd-pipeline-with-github-actions-and-github-pages-in-a-react-app-ij9)。

![](https://res.cloudinary.com/practicaldev/image/fetch/s--a16bXH-z--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9k8vq8yoo4b9uqur4idq.png)

  - 這個示意圖只能就功能面有個印象，細節的設定可以參考[AppleBoy2023][AppleBoy2023]

- 雖然說這個課題已有許多支援與經驗，但因為太新，GPT與Claude都幫不上太多忙，還是得自己爬文測試。以下就重點說明設計的理念。

## docker-compose.yml

- 是使用docker還是專屬的服務來執行act_runner，雖然沒有網友討論過這題，但GPT斬釘截鐵評論：還是docker比較安全。
- docker有很多種執行方式，官網介紹的是 `Dockerfile` 、以下範例是參考[網友][AppleBoy2023]的介紹使用`docker-compose.yml`，
- 有關docker的volumes、runner workflows的目錄，目前都還沒有找到完整的說法，也只能跟Claude討論個大概的架構：
  - docker：是個虛擬機概念，看是誰、在哪裡啟用了它，冒號左邊是啟用者的目錄，冒號右邊是docker的目錄
  - 範例中的docker.sock，基本上不論在虛擬、實體、是workflows環境，都是固定同一個位置。
  - /app，是docker工作的地方，範例沒有預先執行什麼（安裝）程式，如果有，就會是在/app，
  - 而/app定義到workspace的2個位置
- 2個環境變數，參考[AppleBoy2023][AppleBoy2023]的說明，輸入gitea的url、以及要執行runner使用者提供的TOKEN，可以是個人、也可以是組織，以下範例是組織GiteaTeam。
  - 組織不是個能存取gitea repo的單位，但組織的每個成員都可以使用這個docker，不必另外自己再設docker。
- `docker-compose.yml`存放與docker起始的目錄，因為docker不會存取任何檔案，這個位置不會有任何差別。此處放在repo的根目錄，就只是為了將`docker-compose.yml`保存起來

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

- TODO：究竟是docker階段就把node與pnpm準備好、還是每次workflow執行安裝比較好？
  - 如果不涉及插件的安裝，統一在docker執行當然比較有效率。
  - docker沒有repo checkout的功能，找不到package.json，這一條還有待克服。

## main.yml

- 除非另有指定，github/gitea會執行repo `.github/workflows`目錄下所有的`.yml`檔案，只要收到使用者`git push`指令。
- `runs-on`：與前述runner(docker)連結之標籤，可以在gitea的使用者(組織)設定中檢視。
- `uses`：從marketplace拉取image
- `run`：實際執行安裝、編譯及複製等等程序
  - 有關`lockfile`的問題：可能是checkout後所有權的問題、或版本的差異，`pnpm install`時遭遇到困難，GPT建議加一個`--no-frozen-lockfile`設定。
- 要在docker與實體間存取檔案或什麼修改，需使用`ssh`、`scp`、`sftp`等等這類的指令。
  - 登入實體機的密鑰：建議寫在gitea/github設定裏，而不是寫在`yml`檔案，因後者通常是會公開。
  - 因為`scp`內設會嚴格檢查沒有登入過的主機，這會造成屏蔽，需要關閉這項功能。`ssh`似乎沒有這麼嚴格。
  - docker是否可以執行`mount`指令，還需要測試。
- `sshpass`這支程式是自行下載安裝、還是拉取marketlace的image？
  - 後者的功能似乎集中在`ssh`，所謂的`with script`指得是登入遠端主機（實體機）後執行的指令，而不是在虛擬機命令列中執行`sshpass`。
  - 自行安裝也遭遇找不到套件的問題，需要`apt-get update`
- `target`目錄需要和實體apache2的設定結合(`/etc/apache2/site-available/vuepress.conf`)，並且將目錄檔案的權限設定成其他人可閱讀。

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
          export host=$\{\{ secrets.SERVER_HOST \}\}
          export user=$\{\{ secrets.SERVER_USER \}\}
          export pass=$\{\{ secrets.SERVER_PASS \}\}
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

[AppleBoy2023]: https://blog.wu-boy.com/2023/09/introduction-to-gitea-devops-platform/ "初探輕量級 DevOps 平台: Gitea - 台北 DevOpsDay"