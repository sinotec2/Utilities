---
layout: default
title:  anything-llm
parent: API Servers
grand_parent: Web Jokers
last_modified_date: 2024-04-17 09:20:16
tags: API_Server 
---

# anything-llm
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

- [anything-llm](https://blog.darkthread.net/blog/anything-llm)

該網站介紹了一個名為 Anything LLM 的開源專案，它是一個整合了眾多大型語言模型（LLM）API（如ChatGPT、Azure OpenAI、Hugging Face等）的平台。這個平台還整合了多個向量資料庫，並提供了PDF解析、網頁爬取和YouTube影片文字擷取等功能。Anything LLM 使得使用者可以在單一聊天界面中管理多個模型，支持多用戶使用，且可以進行複雜的數據處理和查詢任務。

Anything LLM 使用 MIT 授權，可以透過 Docker 容器輕鬆部署，且無需編程知識即可搭建。它將多個LLM功能和向量資料庫整合到一個界面，降低了技術門檻，但也使得深入研究LLM技術變得更有挑戰性。該平台的目標是為用戶提供一個綜合性的工具，以應對高內捲化的技術環境。

# How to use Dockerized Anything LLM

- [github source](https://github.com/Mintplex-Labs/anything-llm/blob/master/docker/HOW_TO_USE_DOCKER.md)

Use the Dockerized version of AnythingLLM for a much faster and complete startup of AnythingLLM.

### Minimum Requirements

> [!TIP]
> Running AnythingLLM on AWS/GCP/Azure?
> You should aim for at least 2GB of RAM. Disk storage is proportional to however much data
> you will be storing (documents, vectors, models, etc). Minimum 10GB recommended.

- `docker` installed on your machine
- `yarn` and `node` on your machine
- access to an LLM running locally or remotely

\*AnythingLLM by default uses a built-in vector database powered by [LanceDB](https://github.com/lancedb/lancedb)

\*AnythingLLM by default embeds text on instance privately [Learn More](../server/storage/models/README.md)

## Recommend way to run dockerized AnythingLLM!

> [!IMPORTANT]
> If you are running another service on localhost like Chroma, LocalAi, or LMStudio
> you will need to use http://host.docker.internal:xxxx to access the service from within
> the docker container using AnythingLLM as `localhost:xxxx` will not resolve for the host system.
>
> **Requires** Docker v18.03+ on Win/Mac and 20.10+ on Linux/Ubuntu for host.docker.internal to resolve!
>
> _Linux_: add `--add-host=host.docker.internal:host-gateway` to docker run command for this to resolve.
>
> eg: Chroma host URL running on localhost:8000 on host machine needs to be http://host.docker.internal:8000
> when used in AnythingLLM.

> [!TIP]
> It is best to mount the containers storage volume to a folder on your host machine
> so that you can pull in future updates without deleting your existing data!

Pull in the latest image from docker. Supports both `amd64` and `arm64` CPU architectures.

```shell
docker pull mintplexlabs/anythingllm
```

<table>
<tr>
<th colspan="2">Mount the storage locally and run AnythingLLM in Docker</th>
</tr>
<tr>
<td>
  Linux/MacOs
</td>
<td>

```shell
export STORAGE_LOCATION=$HOME/anythingllm && \
mkdir -p $STORAGE_LOCATION && \
touch "$STORAGE_LOCATION/.env" && \
docker run -d -p 3001:3001 \
--cap-add SYS_ADMIN \
-v ${STORAGE_LOCATION}:/app/server/storage \
-v ${STORAGE_LOCATION}/.env:/app/server/.env \
-e STORAGE_DIR="/app/server/storage" \
mintplexlabs/anythingllm
```

</td>
</tr>
<tr>
<td>
  Windows
</td>
<td>

```powershell
# Run this in powershell terminal
$env:STORAGE_LOCATION="$HOME\Documents\anythingllm"; `
If(!(Test-Path $env:STORAGE_LOCATION)) {New-Item $env:STORAGE_LOCATION -ItemType Directory}; `
If(!(Test-Path "$env:STORAGE_LOCATION\.env")) {New-Item "$env:STORAGE_LOCATION\.env" -ItemType File}; `
docker run -d -p 3001:3001 `
--cap-add SYS_ADMIN `
-v "$env:STORAGE_LOCATION`:/app/server/storage" `
-v "$env:STORAGE_LOCATION\.env:/app/server/.env" `
-e STORAGE_DIR="/app/server/storage" `
mintplexlabs/anythingllm;
```

</td>
</tr>
</table>

Go to `http://localhost:3001` and you are now using AnythingLLM! All your data and progress will persist between
container rebuilds or pulls from Docker Hub.

## How to use the user interface

- To access the full application, visit `http://localhost:3001` in your browser.

## About UID and GID in the ENV

- The UID and GID are set to 1000 by default. This is the default user in the Docker container and on most host operating systems. If there is a mismatch between your host user UID and GID and what is set in the `.env` file, you may experience permission issues.

## Build locally from source _not recommended for casual use_

- `git clone` this repo and `cd anything-llm` to get to the root directory.
- `touch server/storage/anythingllm.db` to create empty SQLite DB file.
- `cd docker/`
- `cp .env.example .env` **you must do this before building**
- `docker-compose up -d --build` to build the image - this will take a few moments.

Your docker host will show the image as online once the build process is completed. This will build the app to `http://localhost:3001`.

## Integrations and one-click setups

The integrations below are templates or tooling built by the community to make running the docker experience of AnythingLLM easier.

### Use the Midori AI Subsystem to Manage AnythingLLM

Follow the setup found on [Midori AI Subsystem Site](https://io.midori-ai.xyz/subsystem/manager/) for your host OS
After setting that up install the AnythingLLM docker backend to the Midori AI Subsystem.

Once that is done, you are all set!

## Common questions and fixes

### Cannot connect to service running on localhost!

If you are in docker and cannot connect to a service running on your host machine running on a local interface or loopback:

- `localhost`
- `127.0.0.1`
- `0.0.0.0`

> [!IMPORTANT]
> On linux `http://host.docker.internal:xxxx` does not work.
> Use `http://172.17.0.1:xxxx` instead to emulate this functionality.

Then in docker you need to replace that localhost part with `host.docker.internal`. For example, if running Ollama on the host machine, bound to http://127.0.0.1:11434 you should put `http://host.docker.internal:11434` into the connection URL in AnythingLLM.


### API is not working, cannot login, LLM is "offline"?

You are likely running the docker container on a remote machine like EC2 or some other instance where the reachable URL
is not `http://localhost:3001` and instead is something like `http://193.xx.xx.xx:3001` - in this case all you need to do is add the following to your `frontend/.env.production` before running `docker-compose up -d --build`

```
# frontend/.env.production
GENERATE_SOURCEMAP=false
VITE_API_BASE="http://<YOUR_REACHABLE_IP_ADDRESS>:3001/api"
```

For example, if the docker instance is available on `192.186.1.222` your `VITE_API_BASE` would look like `VITE_API_BASE="http://192.186.1.222:3001/api"` in `frontend/.env.production`.

### Having issues with Ollama?

If you are getting errors like `llama:streaming - could not stream chat. Error: connect ECONNREFUSED 172.17.0.1:11434` then visit the README below.

[Fix common issues with Ollama](../server/utils/AiProviders/ollama/README.md)

### Still not working?

[Ask for help on Discord](https://discord.gg/6UyHPeGZAC)


## Eng06 instance

- user:group $\rightarrow$ 1000:1000
- cmd `$ export STORAGE_LOCATION=$HOME/anythingllm && mkdir -p $STORAGE_LOCATION && touch "$STORAGE_LOCATION/.env" && docker run -d -p 3001:3001 --cap-add SYS_ADMIN -v ${STORAGE_LOCATION}:/app/server/storage -v ${STORAGE_LOCATION}/.env:/app/server/.env -e STORAGE_DIR="/app/server/storage" --ip eng06.sinotech-eng.com mintplexlabs/anythingllm
`
