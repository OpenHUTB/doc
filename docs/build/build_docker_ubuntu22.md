# CARLA Docker 开发环境 (Ubuntu 22.04)

此存储库提供了 **2 种** 不同的基于 Docker 的方法，用于在 **Ubuntu Jammy（22.04）** 上构建和运行 **CARLA（版本 UE4）**：

1. **整体(Monolithic)**  
   - 将虚幻引擎 (UE4) 和 CARLA 捆绑到单个 Docker 镜像中。  
   - 需要漫长的构建过程并产生较大的最终图像（通常 100+ GB）。  
   - 创建一个完全独立的环境，所有内容都在 Docker 内部编译。

2. **轻量级 Devcontainer**
   - 仅安装编译和运行 CARLA 所需的依赖项（加上 NVIDIA 支持）。 
   - 需要将现有的 **UE4** 构建从主机安装到容器中（请参阅 [为 Devcontainer 选项构建 UE4](#build-ue4-prerequisite-for-lightweight-devcontainer) ）。 
   - 构建速度更快，但依赖于本地编译的虚幻引擎文件夹。

在**整体**和**轻量级**之间的选择主要取决于磁盘空间、构建时间以及您是否喜欢完全独立的环境（整体）或重用本地编译的虚幻引擎（轻量级）的设置。

---

## 概述

`Scripts/` 目录中的两个主要脚本负责管理 Docker 容器的构建和启动：

1. **`run_container.sh`**  
   - 通过 `--monolith`（或 `-m`）参数检测**整体**或**轻量级**模式。
   - 如果存在 `--monolith` ，则使用 `carla-ue4.dockerfile`（整体）。否则，默认为 `carla.dockerfile`（轻量级）。

2. **`build_image.sh`**  
   - 一般由`run_container.sh`间接调用。
   - 检查是否提供了 `--monolith` 并选择相应的 Dockerfile。 
   - 处理在单片模式下克隆和构建虚幻引擎所需的 Epic 凭证（来自 `.env` 文件）。 

---

## `Util/Docker/` 中的容器文件(Dockerfiles)

### `carla.dockerfile` (轻量级开发容器 Devcontainer)

- 仅安装 CARLA 依赖项以及 NVIDIA GPU 支持。  
- **不包括**虚幻引擎；相反，必须通过 `UE4_ROOT` 从主机安装预编译的 UE4 文件夹（符合 Carla 的要求）。 
- 非常适合已经拥有兼容 Carla 的 UE4 构建并希望使用更小的镜像进行更快构建的开发人员。 

### `carla-ue4.dockerfile` (整体)

- 从 Epic 的私有 GitHub 克隆虚幻引擎（需要有效的 Epic 凭证）。如果您尚未设置，**请先按照 [本指南](https://www.unrealengine.com/en-US/ue4-on-github) 操作** 。
- 在单个 Docker 镜像中编译 UE4 和 CARLA，该镜像可能超过 100 GB 并且需要数小时才能构建。  
- 该镜像**保留了** `Dist/` 目录，与 `CarlaLegacy.Dockerfile` 相比，您无需使用 `docker_tools.py` 等额外脚本即可运行或提取打包的 CARLA 二进制文件。虽然这会使最终镜像体积较大，但现代硬件通常拥有足够的资源（例如更大的 SSD、更多的 RAM）来处理这种规模。此外，它还消除了反复重建或依赖外部工具的需要。

您可以使用简单的 Docker 命令序列从整体镜像中提取 CARLA 包（将 `0.9.15.2` 替换为您的 CARLA 版本）：

```bash
docker create --name temp_container carla-0.9.15.2-ue4-jammy-dev
docker cp temp_container:/workspaces/carla-0.9.15.2/Dist/CARLA_$(docker run --rm carla-0.9.15.2-ue4-jammy-dev ls /workspaces/carla-0.9.15.2/Dist | grep CARLA_).tar.gz .
docker rm temp_container
```

如果担心磁盘使用情况并且不需要最终打包的工件，则可以注释掉 `carla-ue4.dockerfile` 中的 `make build.utils` 和 `make package`，或者切换到轻量级方法。

---

## 构建 UE4 (轻量级开发容器 Devcontainer 的先决条件)

> 注意: 在尝试克隆之前，请确保您的 GitHub 帐户已链接到 Epic 的 UnrealEngine 存储库。

如果您计划使用**轻量级**方法，则需要在主机上安装一个符合 CARLA 要求（通常为 UE4.26）的**已编译**虚幻引擎文件夹。您有以下两个选项：

### 选项 1：本地构建

关注 CARLA 官方文档：[Unreal Engine - Linux Build](https://carla.readthedocs.io/en/latest/build_linux/#:~:text=wheel%20auditwheel%3D%3D4.0.0-,Unreal%20Engine,-Starting%20with%20version)

### 选项 2: 在构建容器中构建 UE4 

以下步骤概述了在 Docker 容器内构建 UE4 的常规工作流程。有关详细说明，请参阅克隆存储库中的 `Engine/Documentation/Docker/run_with_docker.md` ：

```bash
# 克隆自定义 CarlaUnrealEngine 存储库的示例
git clone git@github.com:wambitz/CarlaUnrealEngine.git CarlaUE4

cd CarlaUE4
Scripts/run_container.sh

# 在容器内遵循官方 UE4.26 构建步骤：
./Setup.sh
./GenerateProjectFiles.sh
make

# 退出容器
exit
```

这些命令会生成所需的虚幻引擎二进制文件，并将其永久存储在您的主机上。您稍后可以在 CARLA 开发容器中重复使用它们。要验证编译是否成功，请在容器内部（或可选地在容器外部）运行以下命令：

```bash
Engine/Binaries/Linux/UE4Editor
```
---

## 脚本使用

### 1. 轻量级模式

此模式依赖于**本地编译**的虚幻引擎文件夹。您需要将该文件夹挂载到用于构建 CARLA 的容器中。

```bash
# 1) 将 UE4_ROOT 设置为主机上现有的 UE4 文件夹：
export UE4_ROOT=/absolute/path/to/UnrealEngine_4.26

# 2) 不使用 --monolith 标志运行容器：
./Scripts/run_container.sh

# 3) 进入容器后，照常构建 CARLA：
./Update.sh
make PythonAPI
make CarlaUE4Editor

# 可选择构建以供分发：
make build.utils
make package
```

- **结果**：  
  - 使用 **`carla.dockerfile`** (轻量级)。  
  - 将主机的 `$UE4_ROOT` 文件夹挂载到容器内的 `/opt/UE4.26` 中。 
  - 需要在主机上安装已完全编译的 UE4。更多详情，请参阅 [为 Devcontainer 选项构建 UE4](#build-ue4-prerequisite-for-lightweight--devcontainer) 。 

### 2. 整体模式

在这种模式下，Docker 克隆并构建虚幻引擎，然后在同一镜像中编译 CARLA。

```bash
# 1) 在 repo 根目录下使用您的 Epic 凭证创建一个 .env 文件：
#    EPIC_USER=YourGitHubUsername
#    EPIC_PASS=YourGitHubToken

# 2) 使用 --monolith 标志运行容器：
./Scripts/run_container.sh --monolith
```

- **结果**：  
  - 使用 **`carla-ue4.dockerfile`**。  
  - 在一个 Docker 镜像中构建 UE4 和 CARLA（通常超过 200 GB）。 
  - 在大多数硬件上需要花费大量时间（数小时）。

---



## 使用 Devcontainer 进行 CARLA 服务器/客户端开发

您可以使用 **Visual Studio Code devcontainer**，并采用轻量级方法。此设置会将主机目录（包括 UE4）挂载到 Docker 环境中。请注意，整体镜像不太适合开发容器，因为它会将所有内容存储在镜像中。

在您的 CARLA 存储库中创建 `.devcontainer/devcontainer.json`：

```jsonc
{
    "name": "CARLA UE4 Dev (jammy)",
    "image": "carla-ue4-jammy-dev",

    "initializeCommand": "./Scripts/build_image.sh",

    // We do NOT need to set "remoteUser" if the Dockerfile's default user is already correct
    // but you can if you want to be explicit. Also "updateRemoteUserUID" can be false, since
    // our Dockerfile already set the user to our exact UID/GID.
    "updateRemoteUserUID": false,

    "customizations": {
      "vscode": {
        "settings": {
          "terminal.integrated.shell.linux": "bash"
        },
        "extensions": [
          "ms-vscode.cpptools"
        ]
      }
    },

    "postStartCommand": "bash",

    // NOTE1: DO NOT pass --user here (we want the Dockerfile default user, not an override)
    // NOTE2: Make sure /usr/share/vulkan/icd.d/nvidia_icd.json exist in the host
    // NOTE3: Ensure UE4_ROOT environment variable is defined in host
    "runArgs": [
      "--rm",
      "--name", "carla-ue4-jammy-devcontainer",
      "--hostname", "carla-devcontainer",
      "--env", "DISPLAY=${localEnv:DISPLAY}",
      "--volume", "/tmp/.X11-unix:/tmp/.X11-unix",
      "--volume", "/usr/share/vulkan/icd.d/nvidia_icd.json:/usr/share/vulkan/icd.d/nvidia_icd.json",
      "--volume", "${localEnv:UE4_ROOT}:/opt/UE4.26",
      "--gpus", "all"
    ]
}
```

### 重要的 Devcontainer 说明

1. **GPU 访问**: 安装并配置 [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) 。
2. **X11 转发**: 确保 `/tmp/.X11-unix` 可访问并且主机上的 `DISPLAY` 设置正确。 
3. **UE4_ROOT 环境变量**: 必须在您的主机上定义，以便 devcontainer 可以挂载 UE4 目录。
4. **Vulkan 支持**: `/usr/share/vulkan/icd.d/nvidia_icd.json` 必须存在于您的主机中，以便 devcontainer 可以挂载 vulkan 配置。

---

## 提示和注意事项

- **NVIDIA GPU**  
  对于硬件加速，请安装 [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

- **磁盘空间**  
  完整镜像可能超过 **200 GB**（例如，某些版本约为 221 GB）。在选择此方案之前，请确保您有足够的空间。

- **构建时间**  
  - 完整模式：在高端工作站（例如，Intel Core i9-14900KF、64 GB RAM、RTX 4090）上大约需要 2 小时。  
  - 轻量级模式：由于重用了本地 UE4 构建，因此速度更快。

- **卷**  
  对于轻量级模式，`$UE4_ROOT` 必须指向已完全编译的 UE4。如果错误或缺失，构建将失败。

- **Epic 凭证**  
  在单片模式下，将 `EPIC_USER` 和 `EPIC_PASS` 存储在项目根目录中的 `.env` 文件中。

- **在主机上运行二进制文件**  
  在容器中构建后，**请勿**在主机上运行 `make launch` 或 `make launch-only`，因为内部容器路径（例如，`/opt/UE4.26`）与您的主机环境不匹配。  
  如果您需要主机访问 CARLA 二进制文件，请首先构建一个发行包（`make build.utils && make package`），然后从主机上的 `Dist/` 中的结果文件运行它们。

- **挂载目录**  
  如果您使用的是 VS Code devcontainers，请避免修改 `/workspaces`，因为这可能会强制重新构建。容器的内部路径通常与主机不同，因此直接在主机上启动会出现问题。


- **`Dist` 文件夹处理**  
   整体模式保留 `Dist` 以便直接使用。如果您需要较小的镜像，请删除或调整 `make build.utils` 和 `make package`。 

---

## 已知问题

1. **`./Update.sh` 中的输出被截断**  
   有时，CARLA 存储库中的 `./Update.sh` 可能会截断日志。一种解决方法是将输出重定向到文件并对其进行尾部处理。

2. **音频支持**  
   ALSA 或 PulseAudio 未预先配置，因此音频功能可能默认不起作用。

3. **UE4Editor 重新构建**  
   在某些情况下，一旦打开 `UE4Editor`（内置于 UE4.26）或使用其构建 CARLA，它可能会拒绝再次打开，除非重新构建。可能会出现缺少插件的错误，这种情况在本地（非 Docker）设置中也会出现。解决方法是使用容器或开发容器从存储库重新构建，或者仔细调整配置文件。

---
