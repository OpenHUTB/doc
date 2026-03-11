# 🦞 Openclaw + DeepSeek Docker 部署教程

---

## 🖥️ 环境信息

| 项目 | 详情 |
|------|------|
| 操作系统 | Windows 11 Home China 25H2 64位 |
| 处理器 | AMD Ryzen 9 7945HX 十六核 |
| 内存 | 16GB DDR5 5200MHz |
| 显卡 | NVIDIA GeForce RTX 5070 Ti Laptop GPU (12GB) |
| Docker | Docker Desktop（官网下载 www.docker.com） |
| AI 模型 | DeepSeek Chat（通过 DeepSeek 官网 API） |

---

## 📋 前置准备

### 1. 安装 Git
前往 https://git-scm.com 下载安装，安装后在 PowerShell 验证：
```powershell
git --version
```

### 2. 安装 Docker Desktop
前往 https://www.docker.com 下载安装，安装后确保 Docker Desktop 已启动。

### 3. 获取 DeepSeek API Key
前往 https://platform.deepseek.com/api_keys 注册并充值，创建 API Key 并保存好。

---

## 🚀 部署步骤

### 第一步：配置 Git 代理（如有需要）

国内网络访问 GitHub 较慢，建议配置代理（端口根据自己的代理软件填写）：

```powershell
git config --global http.proxy http://127.0.0.1:10808
git config --global https.proxy http://127.0.0.1:10808
```

### 第二步：克隆 Openclaw 仓库

```powershell
cd D:\AI   # 切换到你想存放项目的目录
git clone --depth 1 https://github.com/openclaw/openclaw
cd openclaw
```

> `--depth 1` 表示只克隆最新版本，速度更快，节省空间。

### 第三步：配置环境变量

复制模板文件并编辑：

```powershell
Copy-Item .env.example .env
notepad .env
```

在 `.env` 文件中找到并填写以下内容（注意：变量前**不要有空格**）：

```env
OPENAI_API_KEY=sk-你的DeepSeek密钥
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENCLAW_CONFIG_DIR=./config
OPENCLAW_WORKSPACE_DIR=./workspace
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_TOKEN=你自己生成一个随机token
```

> ⚠️ **重要**：变量名前不能有空格！`   OPENAI_API_KEY=xxx`（错误）vs `OPENAI_API_KEY=xxx`（正确）  
> 这是我踩的最深的坑，导致 API Key 一直读取失败。


### 第四步：构建 Docker 镜像

```powershell
docker build -t openclaw:local .
```

> ⏳ 这一步需要较长时间（约 7 分钟），请耐心等待。  
> 如果遇到 `unexpected EOF` 错误，是网络中断导致的，重新运行即可。

### 第五步：修改 docker-compose.yml

用记事本打开 `docker-compose.yml`：

```powershell
notepad docker-compose.yml
```

在 `environment` 部分添加 DeepSeek 相关变量：

```yaml
environment:
  # ... 原有内容保持不变 ...
  OPENAI_API_KEY: ${OPENAI_API_KEY}
  OPENAI_BASE_URL: ${OPENAI_BASE_URL}
```

同时在 `command` 部分末尾加上 `--allow-unconfigured`：

```yaml
command:
  [
    "node",
    "dist/index.js",
    "gateway",
    "--bind",
    "${OPENCLAW_GATEWAY_BIND:-lan}",
    "--port",
    "18789",
    "--allow-unconfigured"
  ]
```

### 第六步：启动容器

```powershell
docker compose up -d
```

验证是否正常运行：

```powershell
docker compose ps
```

看到 `STATUS: Up xx seconds (healthy)` 说明成功。

### 第七步：运行配置向导

```powershell
docker compose run --rm openclaw-cli configure
```

按照向导提示依次配置：
- **Gateway 位置**：选 `Local (this machine)`
- **Model 提供商**：选 `Custom Provider`
- **API Base URL**：填 `https://api.deepseek.com`
- **API Key**：粘贴你的 DeepSeek Key
- **Model ID**：填 `deepseek-chat`
- **Gateway bind**：选 `lan`
- **Gateway token**：填你在 `.env` 里设置的 token（必须一致！）

看到 `Gateway: reachable` 和 `Configure complete` 说明配置成功。

### 第八步：修改 openclaw.json

打开 `config\openclaw.json`，确认以下配置正确：

```json
"agents": {
  "list": [
    {
      "id": "main",
      "model": "custom-api-deepseek-com/deepseek-chat"
    }
  ]
},
"gateway": {
  "bind": "lan",
  "controlUi": {
    "dangerouslyAllowHostHeaderOriginFallback": true
  }
}
```

### 第九步：测试终端对话

```powershell
docker compose run --rm openclaw-cli agent --session-id test01 -m "你好，请自我介绍一下"
```

### 第十步：访问网页界面

浏览器打开 `http://localhost:18789`，在「网关令牌」填入你的 token，点击连接。

首次连接需要批准设备：
```powershell
# 查看待批准设备
docker compose run --rm openclaw-cli devices list

# 批准设备
docker compose run --rm openclaw-cli devices approve <requestId>
```

---

## 🎉 部署成功示例

### 终端对话
![终端对话截图](../img/software/screenshot-cli.png)

### 网页界面
![网页界面截图](../img/software/screenshot-webui.png)

---

## ❗ 常见报错与解决方法

### 错误 1：`pull access denied for openclaw`
**原因**：Docker Hub 上没有公开镜像，需要本地构建。  
**解决**：执行 `docker build -t openclaw:local .`

### 错误 2：`Missing config`（gateway 一直重启）
**原因**：首次启动时没有配置文件。  
**解决**：在 `docker-compose.yml` 的 command 中加入 `--allow-unconfigured`

### 错误 3：`non-loopback Control UI requires gateway.controlUi.allowedOrigins`
**原因**：bind 模式设置为了 `lan` 但没有配置允许的来源。  
**解决**：在 `openclaw.json` 的 `gateway` 部分添加：
```json
"controlUi": {
  "dangerouslyAllowHostHeaderOriginFallback": true
}
```

### 错误 4：`Invalid --bind`
**原因**：`.env` 文件中变量前有多余空格，导致值被读取为空字符串。  
**解决**：检查 `.env` 文件，确保所有变量前没有空格。

### 错误 5：`OPENAI_API_KEY is not set`
**原因**：`.env` 文件中变量名前有空格。  
**解决**：删除变量名前的所有空格。

### 错误 6：`No API key found for provider "anthropic"`
**原因**：Openclaw 默认使用 Anthropic，需要手动切换到 DeepSeek。  
**解决**：运行 `docker compose run --rm openclaw-cli configure`，选择 Custom Provider 并配置 DeepSeek。

### 错误 7：`gateway token mismatch`
**原因**：`.env` 中的 `OPENCLAW_GATEWAY_TOKEN` 和 `openclaw.json` 中的 token 不一致。  
**解决**：确保两处 token 完全一致，或删除 `openclaw.json` 中的 token，只用 `.env` 管理。

### 错误 8：`404 status code (no body)`
**原因**：agent 使用了错误的模型路径（如 `openai/gpt-5.1-codex`）。  
**解决**：在 `openclaw.json` 中将 agent 的 model 改为 `custom-api-deepseek-com/deepseek-chat`。

### 错误 9：`Verification failed: status 402`
**原因**：DeepSeek 账户余额不足。  
**解决**：前往 https://platform.deepseek.com 充值（最低 10 元）。

### 错误 10：`Verification failed: status 401`
**原因**：API Base URL 填写错误（填成了 `http://` 而不是 `https://`）。  
**解决**：确保 API Base URL 为 `https://api.deepseek.com`。

### 错误 11：`unauthorized: gateway token missing`
**原因**：网页界面没有填入 Gateway Token，或填入的 Token 与配置不一致。  
**解决**：
1. 打开 `http://localhost:18789/overview`
2. 在「网关令牌」输入框填入 `.env` 里的 `OPENCLAW_GATEWAY_TOKEN` 值
3. 点击「连接」

### 错误 12：`pairing required`
**原因**：新设备（浏览器）第一次连接 Gateway 需要手动批准。  
**解决**：
```powershell
# 查看待批准设备
docker compose run --rm openclaw-cli devices list

# 批准设备（替换为实际的 Request ID）
docker compose run --rm openclaw-cli devices approve <requestId>
```
批准后刷新网页即可。

### 错误 13：`ERR_EMPTY_RESPONSE`
**原因**：Gateway 绑定模式或 controlUi 配置有问题。  
**解决**：在 `openclaw.json` 的 `gateway` 部分确认：
```json
"bind": "lan",
"controlUi": {
  "dangerouslyAllowHostHeaderOriginFallback": true
}
```
然后重启 Docker。

### 错误 14：`ERR_CONNECTION_REFUSED`
**原因**：`openclaw.json` 格式错误导致容器启动失败。  
**解决**：
1. 用备份文件恢复：
```powershell
copy D:\AI\openclaw\config\openclaw.json.bak D:\AI\openclaw\config\openclaw.json
```
2. 重启 Docker：
```powershell
docker compose down
docker compose up -d
```
3. 修改前先在 [jsonlint.com](https://jsonlint.com) 验证 JSON 格式是否正确。

---

## 🔒 安全注意事项

1. **绝对不要**将 `.env` 文件上传到 GitHub（项目自带的 `.gitignore` 已经排除了它）
2. **绝对不要**在 `openclaw.json` 中硬编码 API Key，应通过环境变量传入
3. API Key 一旦泄露，立刻前往 https://platform.deepseek.com/api_keys 作废并重新生成
4. Gateway Token 泄露后，重新生成并更新 `.env` 文件

---

## 📁 仓库文件说明

```
├── docker-compose.yml   # 修改版：添加了 DeepSeek 环境变量和 --allow-unconfigured
└── .env.example         # 环境变量模板，复制为 .env 后填入真实值
```

---

## 📚 参考资料

- [Openclaw 官方文档](https://docs.openclaw.ai)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [Docker Desktop 官网](https://www.docker.com)

---

## 👤 关于作者

湖南工商大学 机器人工程专业 大一学生，借助 AI 大模型的力量成功完成了这次部署实践。  
欢迎大家进行讨论和复现。  
如有问题欢迎提 Issue 或 PR！
