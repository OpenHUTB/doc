# Ubuntu 24.04 上的 HUTB 构建与验证

本文记录在 **Ubuntu 24.04 LTS** 上从源码构建并运行 HUTB 的完整过程。文中的硬件信息、版本号、文件大小与校验值均取自实际执行的服务器（`yxkj-4U-GPU-Server`），关键步骤均以实际日志核对过。

- [__一、环境说明__](#environment)
- [__二、先决条件__](#prerequisites)
    - [基础依赖](#base-deps)
    - [Ubuntu 24.04 多版本编译器环境搭建](#multi-compiler)
    - [Python 3.12 与虚拟环境](#python-env)
- [__三、获取源码与资产__](#get-source)
- [__四、编译虚幻引擎__](#build-engine)
- [__五、编译 HUTB__](#build-hutb)
    - [boost 1.90.0 依赖包（重点）](#boost)
    - [修改 Setup.sh](#patch-setup)
    - [编译 Python API](#build-pythonapi)
    - [编译服务端](#build-server)
- [__六、运行与验证__](#run-verify)
    - [图形界面启动](#run-gui)
    - [无头启动](#run-headless)
    - [修复 URLab 插件依赖](#fix-libpgm)
    - [修复距离场崩溃](#fix-distancefield)
    - [Python API 联调](#verify-pythonapi)
- [__七、打包__](#package)
- [__八、问题速查表__](#faq)

---

## 一、环境说明 <span id="environment"></span>

| 项目 | 配置 |
| --- | --- |
| 主机名 | `yxkj-4U-GPU-Server` |
| 机型 | 4U GPU Server（主板型号 `60WB32`） |
| 操作系统 | Ubuntu 24.04 LTS（x86_64），内核 `7.0.0-38-generic` |
| CPU | Intel Xeon Gold 6330 @ 2.00 GHz，28 核 / 56 线程（单路） |
| 内存 | 62 GiB |
| 磁盘 | 3.5 TB NVMe（根分区剩余约 2.8 TB） |
| GPU | NVIDIA RTX A6000，49140 MiB 显存 |
| 显卡驱动 | `595.99.02`（专有驱动） |
| 当前生效编译器 | `gcc/g++ 7.5.0`（手动切换）、`clang/clang++ 10.0.1` |
| 系统预装编译器 | `gcc-12`、`g++-12`、`clang-14` |
| 补充编译器 | 源码编译 `GCC 7.5.0`、`LLVM/Clang/LLD 10.0.1` |
| Python | 3.12.3（虚拟环境 `~/hutb_venv`） |
| 目标版本 | HUTB 2.10.1（Carla 分支，虚幻引擎 4.26） |
| 源码路径 | `~/hutb`、`~/UnrealEngine_4.26` |

已验证通过的关键节点：

| 阶段 | 命令 | 验证结果 |
| --- | --- | --- |
| 编译器 | `gcc --version`、`clang --version` | `GCC 7.5.0`、`clang 10.0.1`，`/usr/local/gcc-7`、`/usr/local/llvm-10` 均存在 |
| 引擎编译 | `make`（`~/UnrealEngine_4.26`） | 编译完成，`UE4Editor` 可执行 |
| 依赖包 | boost 1.90.0 | `boost_1_90_0.tar.gz` 201 MB，SHA256 校验通过，`Build/boost-1.90.0-c10-install` 190 MB |
| Python API | `make PythonAPI` | 生成 36.3 MB（36348333 字节）的 `hutb-2.10.1-cp312-cp312-linux_x86_64.whl`，`import carla` 正常 |
| 服务端编译 | `make launch` | 编译错误数为 0，9/9 目标（`CarlaUE4Editor.target`）编译完成，18 个插件 |
| 服务端运行 | `UE4Editor ... -game -RenderOffScreen` | `Initialized CarlaServer: Ports(rpc=2000, streaming=2001, secondary=2002)`，加载 `Town10HD`，端口 2000/2001 处于监听 |
| 稳定性 | 关闭距离场后持续运行 | 连续运行近 30 分钟无崩溃，URLab 插件加载成功，端口保持监听 |
| 打包 | `make package` | `BUILD SUCCESSFUL`、`EXIT_CODE=0`，产物 `Build/UE4Carla/43516c3-dirty` 共 26 GB |
| 打包产物运行 | `LinuxNoEditor/CarlaUE4.sh` | 监听 2000/2001/2002，PythonAPI 连接成功（`Town10HD`），生成 10 辆车流正常 |

---

## 二、先决条件 <span id="prerequisites"></span>

### 基础依赖 <span id="base-deps"></span>

统一安装所有编译所需依赖，避免中途缺包中断：

```sh
sudo apt update
sudo apt install -y build-essential cmake git python3 \
  libgmp-dev libmpfr-dev libmpc-dev \
  gcc-multilib g++-multilib \
  zlib1g-dev g++-10 clang++-10
```

运行与调试还需要以下软件（本文后续步骤会用到）：

```sh
# 无头运行所需的虚拟显示（有真实桌面时可跳过）
sudo apt install -y xvfb

# 引擎依赖下载脚本需要 mono
sudo apt install -y mono-complete
```

### Ubuntu 24.04 多版本编译器环境搭建 <span id="multi-compiler"></span>

- 搭建目标：源码编译安装 **GCC 7.5.0**、**LLVM/Clang/LLD 10.x**，与系统原生编译器多版本共存
- 管理方案：使用 `update-alternatives` 统一管理，禁止直接软链接覆盖系统二进制文件，避免依赖崩坏

#### 1. 源码编译安装 LLVM 10 + Clang + LLD

拉取指定分支源码（国内代理加速）：

```sh
cd ~
git clone --branch release/10.x --recursive https://ghfast.top/https://github.com/llvm/llvm-project.git
```

官方推荐源码外构建，避免污染源码目录，支持多次构建：

```sh
cd llvm-project
mkdir build && cd build
```

CMake 构建配置：

```sh
cmake -G "Unix Makefiles" \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS="clang;lld" \
  -DCMAKE_INSTALL_PREFIX=/usr/local/llvm-10 \
  -DLLVM_INCLUDE_BENCHMARKS=OFF \
  ../llvm
```

关键参数说明：

- `-DLLVM_ENABLE_PROJECTS="clang;lld"`：同时编译 Clang 前端与 LLD 链接器，无需单独构建
- `-DLLVM_INCLUDE_BENCHMARKS=OFF`：关闭基准测试模块，解决高版本 GCC 下 `std::numeric_limits` 头文件缺失报错
- `-DCMAKE_INSTALL_PREFIX=/usr/local/llvm-10`：统一安装路径，与系统环境完全隔离

编译与安装：

```sh
# 自动调用全部 CPU 核心加速编译
make -j$(nproc)
sudo make install
```

验证安装结果：

```sh
/usr/local/llvm-10/bin/clang --version
/usr/local/llvm-10/bin/lld --version
/usr/local/llvm-10/bin/llvm-config --version
```

输出版本号均为 10.x 即为安装成功。

#### 2. 源码编译安装 GCC 7.5.0

下载源码包（华中科大国内镜像）：

```sh
cd ~
# 清理可能存在的不完整下载文件
rm -f gcc-7.5.0.tar.gz
wget http://mirrors.hust.edu.cn/gnu/gcc/gcc-7.5.0/gcc-7.5.0.tar.gz
```

解压源码并创建独立构建目录：

```sh
tar -zxvf gcc-7.5.0.tar.gz
cd gcc-7.5.0
mkdir build && cd build
```

编译配置（适配 Ubuntu 24.04）：

```sh
../configure \
  --prefix=/usr/local/gcc-7 \
  --enable-languages=c,c++ \
  --disable-multilib \
  --disable-werror \
  --disable-libsanitizer \
  --with-system-zlib
```

关键兼容参数说明：

- `--enable-languages=c,c++`：仅编译 C/C++ 编译器，大幅缩减编译时长与踩坑概率
- `--disable-werror`：**核心修复项**，不将编译警告视为错误，解决 90% 以上的高版本系统兼容报错
- `--disable-multilib`：关闭 32 位交叉编译支持，规避 32 位库兼容问题
- `--disable-libsanitizer`：关闭地址消毒模块，避免高版本 glibc 下编译失败

编译与安装：

```sh
make -j$(nproc)
sudo make install
```

验证安装结果：

```sh
/usr/local/gcc-7/bin/gcc --version
/usr/local/gcc-7/bin/g++ --version
```

输出版本号为 7.5.0 即为安装成功。

#### 3. 多版本编译器统一管理

使用 Ubuntu 官方标准工具 `update-alternatives` 管理多版本编译器，支持一键切换、随时回退，完全不破坏系统原生环境。

注册 GCC / G++ 多版本：

```sh
# 注册系统原生 GCC 12，优先级 120（默认优先）
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 120
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 120

# 注册源码编译 GCC 7，优先级 70
sudo update-alternatives --install /usr/bin/gcc gcc /usr/local/gcc-7/bin/gcc 70
sudo update-alternatives --install /usr/bin/g++ g++ /usr/local/gcc-7/bin/g++ 70
```

注册 Clang / Clang++ 多版本：

```sh
# 注册系统原生 Clang 14，优先级 180
sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-14 180
sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-14 180

# 注册源码编译 Clang 10，优先级 200（自动模式下默认选中）
sudo update-alternatives --install /usr/bin/clang clang /usr/local/llvm-10/bin/clang 200
sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/local/llvm-10/bin/clang++ 200
```

!!! 笔记
    本机最终状态：`gcc`/`g++` 为**手动模式**，指向 `/usr/local/gcc-7/bin/gcc`（7.5.0）；`clang`/`clang++` 为**自动模式**，因优先级 200 高于 180，指向 `/usr/local/llvm-10/bin/clang-10`（10.0.1）。可用以下命令核对：

    ```sh
    update-alternatives --display gcc
    update-alternatives --display clang
    ```

版本切换与验证：

```sh
# 切换全局默认版本
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
sudo update-alternatives --config clang
sudo update-alternatives --config clang++

# 验证当前生效版本
gcc --version
g++ --version
clang --version
clang++ --version
```

补充说明：

1. **断点续编**：编译过程中若 SSH 断开，重新连接后进入对应 `build` 目录，重新执行 `make -j$(nproc)` 即可从断点继续，无需重头开始。
2. **优先级规则**：优先级数字越大，自动模式下的默认优先级越高；手动选择版本后优先级规则失效。
3. **使用建议**：日常系统操作保持 GCC 12 为默认版本，编译旧版本项目时临时切换到 GCC 7，避免系统依赖出现异常。
4. **卸载方式**：若需移除源码编译的版本，直接删除 `/usr/local/llvm-10`、`/usr/local/gcc-7` 目录，再执行 `update-alternatives --remove` 移除对应注册项即可。

### Python 3.12 与虚拟环境 <span id="python-env"></span>

Ubuntu 24.04 的系统 Python 为 3.12.3，并启用了 PEP 668 保护，直接 `pip install` 会被拒绝，因此统一使用虚拟环境：

```sh
python3 -m venv ~/hutb_venv
source ~/hutb_venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

本机实测：虚拟环境中为 **numpy 2.5.4**，wheel 构建与 `import carla` 均正常。若编译 Boost.Python 阶段报 numpy 相关错误，再检查并降级到 `pip install "numpy<2"`。

---

## 三、获取源码与资产 <span id="get-source"></span>

```sh
# HUTB 主仓库
git clone https://github.com/OpenHUTB/hutb.git ~/hutb

# Carla 分支的虚幻引擎 4.26
git clone https://github.com/OpenHUTB/engine.git ~/UnrealEngine_4.26
```

下载并解压资产（本机解压后 `Unreal/CarlaUE4/Content/Carla` 约 24 GB，请预留足够磁盘空间）：

```sh
cd ~/hutb
./Update.sh
```

设置虚幻引擎环境变量：

```sh
export UE4_ROOT=~/UnrealEngine_4.26
```

如需持久生效，将上面一行追加到 `~/.bashrc` 后执行 `source ~/.bashrc`。

---

## 四、编译虚幻引擎 <span id="build-engine"></span>

```sh
cd ~/UnrealEngine_4.26
./Setup.sh
./GenerateProjectFiles.sh
make
```

该步骤耗时较长，建议在 `tmux` 会话中执行，防止 SSH 断线中断：

```sh
tmux new -s engine
# 在会话内执行上面的编译命令；断线后 tmux attach -t engine 可继续查看
```

### 常见问题

**1. 脚本没有执行权限**

```text
bash: ./Setup.sh: Permission denied
```

```sh
chmod +x Setup.sh
chmod +x Engine/Build/BatchFiles/Linux/GitDependencies.sh
```

**2. Mono 版本不兼容**

```text
Corlib not in sync with this runtime: expected corlib string (ABB721D6-...) but not found or not string
```

第一步：把引擎自带的旧 Mono 改名隐藏，强制使用系统 Mono：

```sh
mv Engine/Binaries/ThirdParty/Mono/Linux Engine/Binaries/ThirdParty/Mono/Linux_broken
```

第二步：用系统 `mono` 运行依赖下载程序（支持断点续传）：

```sh
mono Engine/Binaries/DotNET/GitDependencies.exe --prompt
```

第三步：为下载得到的脚本补上可执行权限：

```sh
find . -type f -name "*.sh" -exec chmod +x {} \;
```

第四步：用空白配置覆盖旧版工具生成的 `.config`，避免 `UnrealBuildTool` 崩溃：

```sh
# 1. 制作一个干净的配置文件空壳
echo '<?xml version="1.0" encoding="utf-8" ?><configuration></configuration>' > clean.config
# 2. 先查看系统到底找出了哪些文件，确认无误后再覆盖源码模板
find Engine/Source/Programs -name "App.config"
find Engine/Source/Programs -name "App.config" -exec cp clean.config {} \;
# 3. 再覆盖已经生成的配置
find Engine/Binaries/DotNET -name "*.config"
find Engine/Binaries/DotNET -name "*.config" -exec cp clean.config {} \;
```

**3. `make` 时内存不足**

引擎默认使用全部 CPU 核心并行编译，内存不足时会被系统杀死。可编辑
`~/UnrealEngine_4.26/Engine/Saved/UnrealBuildTool/BuildConfiguration.xml`，限制并行核数：

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
  <BuildConfiguration>
    <ProcessorCountMultiplier>7</ProcessorCountMultiplier>
    <MaxParallelActions>7</MaxParallelActions>
    <bAllowParallelExecutor>true</bAllowParallelExecutor>
  </BuildConfiguration>
  <SNDBS>
    <ProcessorCountMultiplier>4</ProcessorCountMultiplier>
    <MaxProcessorCount>4</MaxProcessorCount>
  </SNDBS>
  <ParallelExecutor>
    <ProcessorCountMultiplier>7</ProcessorCountMultiplier>
    <MaxProcessorCount>7</MaxProcessorCount>
    <bStopCompilationAfterErrors>true</bStopCompilationAfterErrors>
  </ParallelExecutor>
</Configuration>
```

核数请根据自己的硬件配置调整。编译完成后可用以下命令验证引擎是否正常：

```sh
# 有屏渲染
cd ~/UnrealEngine_4.26/Engine/Binaries/Linux && ./UE4Editor

# 无屏渲染
cd ~/UnrealEngine_4.26/Engine/Binaries/Linux && ./UE4Editor -RenderOffScreen -unattended -nosplash -nop4
```

!!! 注意
    若出现 `InitSDL() failed, cannot create application instance`，说明当前会话没有可用的图形显示，请改用上面的无屏渲染命令，或在 SSH 会话中先执行 `export DISPLAY=:1`（服务器已登录桌面时）。

---

## 五、编译 HUTB <span id="build-hutb"></span>

以下命令均在 HUTB 根目录（`~/hutb`）执行。

### boost 1.90.0 依赖包（重点）<span id="boost"></span>

`make PythonAPI` 会先编译 Boost.Python。`Setup.sh` 中固定了版本：

```sh
BOOST_VERSION=1.90.0
BOOST_PACKAGE_BASENAME=boost_1_90_0
```

也就是需要下载 **`boost_1_90_0.tar.gz`**（约 201 MB）。在本机整个构建过程中，这一步耗时最多、反复最多，必须单独说明。

最终可用的源包（已核对）：

| 项目 | 实测值 |
| --- | --- |
| 文件路径 | `~/hutb/Build/dependencies/src/boost_1_90_0.tar.gz` |
| 文件大小 | `210975925` 字节（约 201 MiB） |
| SHA256 | `5e93d582aff26868d581a52ae78c7d8edf3f3064742c6e77901a1f18a437eea9` |
| 校验结果 | 与 `Setup.sh` 中的 `BOOST_SHA256SUM` 完全一致 |
| 编译产物 | `~/hutb/Build/boost-1.90.0-c10-install`（190 MB，含 `libboost_python` 等） |

校验方法：

```sh
sha256sum ~/hutb/Build/dependencies/src/boost_1_90_0.tar.gz
```

下载过程中实际踩过的坑：

1. **代理返回 404**：用 `ghfast.top` 代理下载 GitHub Release 资产时，因 release 资产命名与 URL 不匹配直接 404。
2. **单线程下载极慢**：改用官方 `archives.boost.io` 源、单线程 `wget`，速率只有约 **44 KB/s**，201 MB 耗时 **1 小时 19 分 44 秒**；另一次 116 MB 的包耗时 **6 分 41 秒**（约 297 KB/s）。
3. **文件“下载完却找不到”**：`wget` 残留的半成品文件、`aria2c` 对同名文件自动重命名（追加 `.1`/`.2`），导致误以为下载失败而重复下载，进一步拉长了时间。
4. **最终成功的方式**：用 `aria2c` 16 线程断点续传，同样从 `archives.boost.io` 下载，**13 秒完成**（约 **27 MB/s**）。

推荐下载命令：

```sh
cd ~/hutb/Build && mkdir -p dependencies/src
aria2c -x 16 -s 16 -c -o boost_1_90_0.tar.gz \
  https://archives.boost.io/release/1.90.0/source/boost_1_90_0.tar.gz
sha256sum boost_1_90_0.tar.gz
mv boost_1_90_0.tar.gz dependencies/src/
```

!!! 重要
    本项目对 `Setup.sh` 做了改造：优先使用 `dependencies/src/boost_1_90_0.tar.gz` 本地包（校验通过则完全不联网）；本地包缺失或校验失败时才依次回退到 boost 官网、CARLA 的 backblaze 备份。这样换机器或重编时不必再次经历上面的下载过程。

对应逻辑（`Util/BuildTools/Setup.sh`）：

```sh
BOOST_PACKAGE_BASENAME=boost_${BOOST_VERSION//./_}

# 优先使用本地包
if [ -f "dependencies/src/${BOOST_PACKAGE_BASENAME}.tar.gz" ] ; then
  cp "dependencies/src/${BOOST_PACKAGE_BASENAME}.tar.gz" .
fi

# 本地包缺失或校验不通过时，从 boost 官网下载
if [ ! -f "${BOOST_PACKAGE_BASENAME}.tar.gz" ] || \
   [[ $(sha256sum "${BOOST_PACKAGE_BASENAME}.tar.gz" | cut -d " " -f 1) != "${BOOST_SHA256SUM}" ]] ; then
  wget "https://archives.boost.io/release/${BOOST_VERSION}/source/${BOOST_PACKAGE_BASENAME}.tar.gz" \
    -O ${BOOST_PACKAGE_BASENAME}.tar.gz || true
fi
```

### 修改 Setup.sh <span id="patch-setup"></span>

!!! 警告
    本机对 `Util/BuildTools/Setup.sh` 的实际修改共两处，否则依赖编译失败：
    1. 构建 boost 时，执行 `./bootstrap.sh` 的命令中去掉了 `--with-toolset=clang` 选项；
    2. 对 rpclib 执行 cmake 时，去掉了 `-stdlib=libc++` 选项。

### 编译 Python API <span id="build-pythonapi"></span>

```sh
cd ~/hutb
source ~/hutb_venv/bin/activate
make PythonAPI ARGS="--python-version=3.12"
```

编译完成后在 `PythonAPI/carla/dist` 下生成 wheel，本机实际产物为：

```text
hutb-2.10.1-cp312-cp312-linux_x86_64.whl
```

安装并验证：

```sh
pip install PythonAPI/carla/dist/hutb-2.10.1-cp312-cp312-linux_x86_64.whl
python -c "import carla; print('carla ok')"
```

!!! 注意
    本机使用 Python 3.12.3 虚拟环境，numpy 为 2.5.4，wheel 构建与导入均正常。若编译 Boost.Python 时报 NumPy 相关错误，先执行 `python3 -m pip show numpy` 确认版本，必要时降级到 `numpy<2` 再编译。

### 编译服务端 <span id="build-server"></span>

```sh
cd ~/hutb
export UE4_ROOT=~/UnrealEngine_4.26
make launch
```

本机验证结果：**编译错误数为 0，9/9 目标（`CarlaUE4Editor.target`）编译完成**，产物为 `Unreal/CarlaUE4/Binaries/Linux/libUE4Editor-CarlaUE4.so`，`Unreal/CarlaUE4/Plugins` 下共 **18 个插件**。

!!! 笔记
    `make launch` 只完成编译并不代表编辑器一定能启动。本机在无图形会话中执行时，编译全部通过，但编辑器报 `InitSDL() failed, cannot create application instance` 后退出（`make` 返回错误 1）。此时需先 `export DISPLAY=:1`（服务器已登录桌面），或在 SSH 中使用 `xvfb-run`，或改用下文的 `-RenderOffScreen` 无头启动。

如遇大面积报错 `error opening .../wd4103: Not a directory`（AirSim 脚本携带 Windows 专属的 `/wd4103` 参数），按以下步骤处理：

```sh
# 1. 抹除 Carla 与 UE4 源码中的该参数
find ~/UnrealEngine_4.26/Engine/Source/Programs/UnrealBuildTool -type f -name "*.cs" -exec sed -i 's/-wd4103//g' {} +
find ~/UnrealEngine_4.26/Engine/Source/Programs/UnrealBuildTool -type f -name "*.cs" -exec sed -i 's/\/wd4103//g' {} +
find ~/hutb -type f -name "*.cs" -exec sed -i 's/-wd4103//g' {} +
find ~/hutb -type f -name "*.cs" -exec sed -i 's/\/wd4103//g' {} +

# 2. 删除旧的构建工具与受污染的中间文件，重新生成
rm -f ~/UnrealEngine_4.26/Engine/Binaries/DotNET/UnrealBuildTool.exe
cd ~/UnrealEngine_4.26 && ./GenerateProjectFiles.sh
rm -rf ~/UnrealEngine_4.26/Engine/Intermediate/Build/Linux/B4D820EA
rm -rf ~/hutb/Unreal/CarlaUE4/Intermediate
```

若编译成功但启动时进程被杀死（Error 137），说明内存不足，可临时增加交换空间并限制着色器编译线程：

```sh
sudo fallocate -l 4G /swapfile_temp
sudo chmod 600 /swapfile_temp
sudo mkswap /swapfile_temp
sudo swapon /swapfile_temp
```

并在 `~/UnrealEngine_4.26/Engine/Config/BaseEngine.ini` 中设置 `NumUnusedShaderCompilingThreads=12`（保留 12 个核心不参与着色器编译，按硬件调整）。

---

## 六、运行与验证 <span id="run-verify"></span>

### 图形界面启动 <span id="run-gui"></span>

```sh
cd ~/hutb
./BuildCarlaUE4.sh --launch
```

!!! 警告
    **UE4.26 桌面端已移除 OpenGL，`--opengl` / `-opengl` 不会生效。**
    `Util/BuildTools/BuildCarlaUE4.sh` 仍然接受 `--opengl`（第 62 行会转成 `-opengl`），
    但引擎在 `Engine/Source/Runtime/RHI/Private/Linux/LinuxDynamicRHI.cpp` 中只把 OpenGL 留给移动端预览。
    桌面模式收到该参数会弹出
    `Warning: OpenGL is no longer supported for desktop platforms. Vulkan will be used instead.`，
    随后清除标志并继续使用 Vulkan，图形界面只能用 Vulkan 后端。

    本机驱动 `595.99.02` 下该后端不稳定：启动约 7 分钟后渲染线程崩溃，
    此时显存占用仅 673 MB，并非显存不足：

    ```text
    Unhandled Exception: SIGSEGV
    libUE4Editor-VulkanRHI.so!FVulkanMemoryManager::...
    ```

    已验证稳定的运行方式是无头启动（`-game -RenderOffScreen`，见下一节）并关闭距离场；
    图形界面的长时间稳定性尚未验证。

首次启动需要编译 1 万多个着色器并构建网格距离场，耗时较长，期间日志会持续输出 `shaders left to compile`，属于正常现象。后续启动因有 DDC 缓存会快很多。若也在启动若干帧后遇到距离场崩溃，按[第六节](#fix-distancefield)关闭距离场即可。

### 无头启动 <span id="run-headless"></span>

没有图形界面或不想打开编辑器时，可直接以游戏模式启动专用服务器：

```sh
cd ~/hutb/Unreal/CarlaUE4

DISPLAY=:1 \
LD_LIBRARY_PATH=~/UnrealEngine_4.26/Engine/Binaries/Linux:~/hutb/Unreal/CarlaUE4/Plugins/UnrealRoboticsLab/Binaries/Linux \
~/UnrealEngine_4.26/Engine/Binaries/Linux/UE4Editor CarlaUE4.uproject \
  -game -RenderOffScreen -nosound -carla-rpc-port=2000
```

当初实际执行的命令里还带了 `-opengl`；该参数在 UE4.26 桌面端会被忽略并继续使用 Vulkan（见上一节），因此这里等价于不传。

建议同样放在 `tmux` 中运行，并把输出重定向到日志：

```sh
tmux new -d -s sim "cd ~/hutb/Unreal/CarlaUE4 && DISPLAY=:1 \
LD_LIBRARY_PATH=~/UnrealEngine_4.26/Engine/Binaries/Linux:~/hutb/Unreal/CarlaUE4/Plugins/UnrealRoboticsLab/Binaries/Linux \
~/UnrealEngine_4.26/Engine/Binaries/Linux/UE4Editor CarlaUE4.uproject \
  -game -RenderOffScreen -nosound -carla-rpc-port=2000 > /tmp/hutb_sim.log 2>&1"

tail -f /tmp/hutb_sim.log
```

启动成功的标志：

```text
LogCarlaServer: Initialized CarlaServer: Ports(rpc=2000, streaming=2001, secondary=2002)
LogCarlaServer: New episode 'Town10HD' started
LogTemp: SimWorldGameMode: AirSim bootstrap complete. API server started.
```

检查端口监听：

```sh
ss -tln | grep -E ":2000|:2001"
```

```text
LISTEN 0 4096 0.0.0.0:2000 0.0.0.0:*
LISTEN 0 4096 0.0.0.0:2001 0.0.0.0:*
```

### 修复 URLab 插件依赖 <span id="fix-libpgm"></span>

首次启动时若出现：

```text
LogCore: Warning: dlopen failed: libpgm-5.2.so.0: cannot open shared object file: No such file or directory
ModuleManager: Unable to load module '.../Plugins/UnrealRoboticsLab/Binaries/Linux/libUE4Editor-URLab.so'
```

说明 `URLab` 插件依赖 `libpgm-5.2`，而 Ubuntu 24.04 只提供 `libpgm-5.3`。二者 ABI 兼容，可做兼容软链并把库放到插件目录：

```sh
sudo ln -sf /lib/x86_64-linux-gnu/libpgm-5.3.so.0 /usr/lib/x86_64-linux-gnu/libpgm-5.2.so.0
sudo ldconfig

cp /lib/x86_64-linux-gnu/libpgm-5.3.so.0 \
   ~/hutb/Unreal/CarlaUE4/Plugins/UnrealRoboticsLab/Binaries/Linux/libpgm-5.2.so.0
```

修改后需要重启服务端才能生效。修复后日志中会出现：

```text
LogURLab: Registered MuJoCo Asset Category with bitmask: 8192
```

### 修复距离场崩溃 <span id="fix-distancefield"></span>

服务端启动后、渲染若干帧（约 400~700 帧）时，可能出现如下崩溃：

```text
Unhandled Exception: SIGSEGV: invalid attempt to read memory at address 0x...
libUE4Editor-Engine.so!FDistanceFieldVolumeTexture::IsValidDistanceFieldVolume() const
libUE4Editor-Engine.so!FPrimitiveSceneShaderData::FPrimitiveSceneShaderData(...)
libUE4Editor-Renderer.so!UpdateGPUSceneInternal<FRWBufferStructured>(...)
```

原因是首次运行时现场生成网格距离场（distance field），部分网格的距离场数据无效，导致 GPU Scene 更新时崩溃。距离场仅用于阴影与环境光遮蔽等视觉效果，关闭后不影响仿真与 Python API。编辑 `~/hutb/Unreal/CarlaUE4/Config/DefaultEngine.ini`：

```ini
[/Script/Engine.RendererSettings]
r.GenerateMeshDistanceFields=False
r.DistanceFieldShadowing=0
r.DistanceFieldAO=0
```

修改前建议先备份：

```sh
cp ~/hutb/Unreal/CarlaUE4/Config/DefaultEngine.ini \
   ~/hutb/Unreal/CarlaUE4/Config/DefaultEngine.ini.bak
```

修改后重新启动服务端。本机实测：关闭距离场后服务端已连续运行近 30 分钟，**0 次崩溃**，`rpc=2000`/`streaming=2001` 端口持续监听，`Town10HD` 地图正常加载。

### Python API 联调 <span id="verify-pythonapi"></span>

服务端保持运行，另开终端：

```sh
source ~/hutb_venv/bin/activate
cd ~/hutb/PythonAPI/examples
pip install -r requirements.txt

# 生成车流
python generate_traffic.py

# 切换天气
python dynamic_weather.py
```

能够连接 `localhost:2000` 并生成车辆、天气随时间变化，即表示客户端与服务端联通正常。

---

## 七、打包 <span id="package"></span>

```sh
cd ~/hutb
export UE4_ROOT=~/UnrealEngine_4.26
export UE_USE_SYSTEM_MONO=1
make package
```

产物位于 `Build/UE4Carla/<package_id>/`（本机目标路径为 `Build/UE4Carla/43516c3-dirty`）。

实测结果：

| 项目 | 结果 |
| --- | --- |
| UAT 结束状态 | `BUILD SUCCESSFUL`，`EXIT_CODE=0` |
| 产物大小 | 26 GB（`LinuxNoEditor` 占 26 GB） |
| Cook 中间产物 | `Saved/Cooked` 约 24 GB |
| 可执行入口 | `LinuxNoEditor/CarlaUE4.sh` |
| 启动后监听端口 | 2000（RPC）、2001（streaming）、2002（secondary） |

!!! 注意
    `make package` 在非交互式 shell（如 `tmux`）中执行时必须显式 `export UE4_ROOT`，否则会提示 `UE4_ROOT is not defined`。

!!! 注意
    `UE_USE_SYSTEM_MONO=1` 不能省略：引擎自带 mono 4.5 的 libs 与系统 mono 6.8 混用会抛 `System.Native` 的 `DllNotFoundException`，UAT 在编译 AutomationTool 阶段就会退出。

### 报错：AutomationTool failed to compile

```text
>>>> xbuild tool is deprecated and will be removed in future updates, use msbuild instead <<<<
RunUAT ERROR: AutomationTool failed to compile.
```

根因是 `RunUAT.sh` 使用 `/p:TargetPlatformProfile=` 等完整参数调用 `xbuild`，而 mono 6.8 的 `xbuild` 会报 `MSBUILD0004: Too many project files specified`。可用最小参数手动编译一次 AutomationTool：

```sh
xbuild ~/UnrealEngine_4.26/Engine/Source/Programs/AutomationTool/AutomationTool.csproj \
  /p:Configuration=Development
```

产物为 `~/UnrealEngine_4.26/Engine/Binaries/DotNET/AutomationTool.exe`。

随后在 `Util/BuildTools/Package.sh` 的 BuildCookRun 参数中加入 `-nocompile` 与 `-nocompileeditor`，跳过重复编译：

```sh
      -nocompileeditor -nocompile -nop4 -cook -stage -archive -package -iterate \
```

再重新执行 `make package`。

### 报错：加载平台脚本 DLL 失败

```text
Failed to load script DLL: .../Engine/Binaries/DotNET/AutomationScripts/AllDesktop.Automation.dll
```

同样的报错会依次出现在 `Android`、`BuildGraph`、`TVOS` 等平台脚本上。原因是源码分发中 `Engine/Source/Programs/AutomationScripts` 下的平台工程从未被编译。逐个编译 16 个工程：

```sh
cd ~/UnrealEngine_4.26/Engine/Source/Programs/AutomationScripts
for p in *.Automation.csproj; do
  xbuild "$p" /p:Configuration=Development /p:Platform=AnyCPU \
    /p:LangVersion=7.2 /p:WarningLevel=0 /p:NoWarn=1591
done
```

- `/p:LangVersion=7.2`：规避 mono 默认语言版本下的 `CS1519`/`CS1525` 语法错误。
- `/p:WarningLevel=0`：`CS0219` 等警告被当作错误（warnings as errors）时直接降级。
- 若 `AutomationScripts.Automation.csproj` 编译 `SyncBinariesFromUGS.Automation.cs` 报语法错误（第 271 行多写了一个 `};`），把该行改为 `}`，或从工程文件的 `<Compile Include=...>` 中排除该项。

产物在 `Engine/Binaries/DotNET/AutomationScripts/`，上述报错随之消失。

### 报错：Shipping 链接重复定义 `__isoc23_strtol`

```text
ld: duplicate symbol '__isoc23_strtol' in ...
```

Ubuntu 24.04 的 glibc 2.38 起提供了 `__isoc23_*` 系列符号，而 HUTB 自带的 glibc 兼容 shim 又定义了一遍。给 shim 中的定义加弱符号即可：

```cpp
__attribute__((weak)) long int __isoc23_strtol(const char *nptr, char **endptr, int base)
```

本机共修改 3 个文件、8 个符号：

- `Unreal/CarlaUE4/Source/CarlaUE4/GlibcCompat.cpp`
- `Unreal/CarlaUE4/Plugins/CarlaTools/Source/CarlaTools/GlibcCompat.cpp`
- `Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Carla.cpp`（6 个 `__isoc23_*`）

### 报错：Cook 结束 `ExitCode=1`

Cook 结束后 UAT 报 `ExitCode=1` 并中止后续 `stage`/`archive`/`package`。本机日志中的判定来源是 DReyeVR 插件资源“too old / unversioned”，但 `Saved/Cooked` 已完整产出（约 24 GB）。确认 Cooked 内容完整后，可先跳过 Cook，只跑后三个阶段：把 `Util/BuildTools/Package.sh` 中的

```sh
      -nocompileeditor -nocompile -nop4 -cook -stage -archive -package -iterate \
```

临时改为

```sh
      -nocompileeditor -nocompile -nop4 -skipcook -stage -archive -package -iterate \
```

验证通过后再恢复 `-cook`。

### 报错：Stage 阶段 `DirectoryNotFoundException`

```text
System.IO.DirectoryNotFoundException: Couldn't find .../Content/Carla/RoadRunner/Maps/OpenDrive
```

`DefaultGame.ini` 的 `DirectoriesToAlwaysStageAsUFS` 中声明了以下目录，但源码树里并不存在，UAT 复制时直接失败：

```sh
cd ~/hutb/Unreal/CarlaUE4
mkdir -p Content/Carla/RoadRunner/Maps/OpenDrive
mkdir -p Content/roadrunner/map/OpenDrive
mkdir -p Content/roadrunner/ccsp
```

补齐空目录后重新执行 stage/package 即可。

### 报错：产物启动缺 `libmujoco.so.3.7.0`

```text
error while loading shared libraries: libmujoco.so.3.7.0: cannot open shared object file
```

打包产物里的 MuJoCo 目录只带了 `libmujoco.so` 软链，缺少实际目标文件。从源码树复制：

```sh
cp ~/hutb/Unreal/CarlaUE4/Plugins/UnrealRoboticsLab/third_party/install/MuJoCo/lib/libmujoco.so.3.7.0 \
   ~/hutb/Build/UE4Carla/43516c3-dirty/LinuxNoEditor/CarlaUE4/Plugins/UnrealRoboticsLab/third_party/install/MuJoCo/lib/
```

### 使用打包产物运行

```sh
cd ~/hutb/Build/UE4Carla/43516c3-dirty/LinuxNoEditor
export LD_LIBRARY_PATH=$PWD/CarlaUE4/Plugins/UnrealRoboticsLab/third_party/install/MuJoCo/lib:$LD_LIBRARY_PATH
./CarlaUE4.sh -RenderOffScreen -nosound -carla-rpc-port=2000
```

实测启动日志末尾：

```text
Initialized CarlaServer: Ports(rpc=2000, streaming=2001, secondary=2002)
...
SimpleFlight
Resizing viewport due to setres change, 1024 x 768
```

`ss -tln` 中 2000/2001/2002 均在监听，进程 `CarlaUE4-Linux-Shipping` 持续运行。

!!! 注意
    启动打包产物前先退出编辑器（`pkill -f "UE4Editor /home/yxkj/hutb"`），否则 2000 端口被占用会报 `bind: Address already in use`。

#### 打包产物联调

```sh
source ~/hutb_venv/bin/activate
python - <<'PY'
import carla
c = carla.Client('localhost', 2000)
c.set_timeout(30)
w = c.get_world()
print(c.get_server_version(), w.get_map().name, len(w.get_actors()))
print(w.get_weather())
PY
```

实测输出：

```text
43516c3-dirty Carla/Maps/Town10HD 24
WeatherParameters(cloudiness=20.000000, precipitation=0.000000, ...)
```

在打包产物上生成、销毁车辆均成功，官方车流示例同样可用：

```sh
cd ~/hutb/PythonAPI/examples
python generate_traffic.py -n 10 -w 0 --port 2000
```

输出 `spawned 10 vehicles and 0 walkers`，车流在打包版中正常运行。

---

## 八、问题速查表 <span id="faq"></span>

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `libpgm-5.2.so.0: cannot open shared object file` | Ubuntu 24.04 仅有 `libpgm-5.3` | 软链 5.2 到 5.3，并复制到插件 `Binaries/Linux` |
| 启动约 7 分钟后 `SIGSEGV`，栈在 `FVulkanMemoryManager` | UE4.26 桌面端已移除 OpenGL，`-opengl` 会被引擎忽略并继续使用 Vulkan；驱动 `595.99.02` 下 Vulkan 后端不稳定 | 用 `-game -RenderOffScreen` 无头运行并关闭距离场（已验证稳定近 30 分钟）；`--opengl` / `-opengl` 无效 |
| `FDistanceFieldVolumeTexture::IsValidDistanceFieldVolume` 崩溃 | 运行时生成的距离场数据无效 | 关闭 `r.GenerateMeshDistanceFields` 等距离场特性 |
| `UE4_ROOT is not defined` | 非交互式 shell 未加载 `.bashrc` | 显式 `export UE4_ROOT` |
| `RunUAT ERROR: AutomationTool failed to compile` | mono 6.8 的 `xbuild` 参数不兼容 | 手动 `xbuild` 编译 AutomationTool，并在 Package.sh 加 `-nocompile` |
| UAT 报 `System.Native` 的 `DllNotFoundException` | 引擎自带 mono 4.5 与系统 mono 6.8 混用 | `export UE_USE_SYSTEM_MONO=1` 后重跑 |
| `Failed to load script DLL ... AutomationScripts/*.Automation.dll` | 平台脚本工程从未编译 | 逐个 `xbuild` 编译 `Engine/Source/Programs/AutomationScripts` 下的工程 |
| `ld: duplicate symbol '__isoc23_strtol'` | glibc 2.38+ 与自带兼容 shim 重复定义 | 给 shim 中的 `__isoc23_*` 加 `__attribute__((weak))` |
| Cook 结束 `ExitCode=1`，`stage` 未执行 | DReyeVR 资源版本过旧 | Cooked 完整时用 `-skipcook -stage -archive -package` 续跑 |
| Stage 报 `DirectoryNotFoundException: .../OpenDrive` | `DirectoriesToAlwaysStageAsUFS` 目录在源码树缺失 | `mkdir -p` 补齐 3 个 OpenDrive/ccsp 目录 |
| 产物启动报 `libmujoco.so.3.7.0: cannot open shared object file` | 产物中只有软链，缺目标文件 | 从源树复制 `libmujoco.so.3.7.0` 并设置 `LD_LIBRARY_PATH` |
| 启动打包产物报 `bind: Address already in use` | 编辑器仍占用 2000 端口 | 先 `pkill -f "UE4Editor /home/yxkj/hutb"` |
| `import carla` 报 NumPy 相关错误 | 环境中的 numpy 版本不兼容 | 在虚拟环境中降级到 `numpy<2` |
| `InitSDL() failed` | 当前会话无图形显示 | 设置 `DISPLAY`、使用 xvfb 或 `-RenderOffScreen` |
