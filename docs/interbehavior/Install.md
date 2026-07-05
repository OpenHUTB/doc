# 在构建的Carla 0.9.13工作空间中安装 `DReyeVR`

## 要求
- 确保您的机器满足 Carla 要求的先决条件： [Windows](https://carla.readthedocs.io/en/0.9.13/build_windows), [Linux](https://carla.readthedocs.io/en/0.9.13/build_linux), [Mac*](https://github.com/GustavoSilvera/carla/blob/m1/Docs/build_mac.md)
- **重要**：如果在 **Windows** 上，则 **需要** [`Make-3.81`](https://gnuwin32.sourceforge.net/packages/make.htm) ，如 [Carla 文档](https://carla.readthedocs.io/en/latest/build_windows/#system-requirements) 所述
- 如果你之前已经在 PYTHONPATH 中安装了 Carla，则需要删除所有之前的 PythonAPI 安装
  - 例如，如果您 [通过 pip 安装了 carla](https://pypi.org/project/carla/) ，则 **需要将其卸载** 才能继续。
    ```bash
    pip uninstall carla
    ```

## 开始 Getting started
- 应该首先保证 DReyeVR 已经下载：
  ```bash
  git clone https://github.com/HARPLab/DReyeVR --depth 1
  ```
- 首先需要从源代码安装虚 [幻引擎 4.26（CARLA fork）](https://github.com/CarlaUnreal/UnrealEngine) 
  ```bash
  git clone https://github.com/CarlaUnreal/UnrealEngine
  # 将此位置设置为您的 $UE4_ROOT 环境变量
  ```

  **重要** 在 DReyeVR for Carla 0.9.13 上，您需要将 UE4 存储库恢复为受支持的版本（用于 DReyeVR）。这是为了优化 DX11 渲染性能，在我们的测试中，DX11 是 VR 的最佳渲染后端。
  ```bash
  # in $UE4_ROOT
  git checkout d40ec35474e8793b4eea60dba6c4f051186e458e
  # or git reset --hard d40ec35474e8793b4eea60dba6c4f051186e458e
  ```

  - **重要：** 如果 `git clone` 链接对您不起作用，您可能需要 [加入 Epic Games 组织](https://www.unrealengine.com/en-US/ue4-on-github) 才能访问 UnrealEngine 及其所有分支。
  - 适用于您的系统的 UE4 构建说明可在此处找到：[Windows](https://carla.readthedocs.io/en/0.9.13/build_windows/#unreal-engine) 、[Linux](https://carla.readthedocs.io/en/0.9.13/build_linux/#unreal-engine) 、[Mac*](https://github.com/GustavoSilvera/carla/blob/m1/Docs/build_mac.md#unreal-engine-fork) 
  <!-- - 注意：我们只保留了 Carla 分支的我们自己的 HARPLab 分支，以保持版本兼容性并启用 Carla 不需要的次要功能（例如，注视点渲染）。  -->
  - 为了成功运行 `Setup.sh`，您需要下载并替换 `/Engine/Build` 中的 Commit.gitdeps.xml 文件。请参阅 [Commit.gitdeps.xml](https://github.com/HARPLab/UnrealEngine/blob/DReyeVR-0.9.13/Engine/Build/Commit.gitdeps.xml) 中更新的 XML 文件（注意：该链接已经失效，可以使用 [这个文件](https://github.com/EpicGames/UnrealEngine/blob/4.26/Engine/Build/Commit.gitdeps.xml) ）

<!-- vanilla 原意是指原味、香草，引申义就是原始的、最初的版本 --> 
- 然后你需要克隆并构建一个 [vanilla Carla 0.9.13](https://carla.readthedocs.io/en/0.9.13/#building-carla) 
  ```bash
  git clone https://github.com/carla-simulator/carla -b 0.9.13 --depth 1
  ```
  - 使用 [Building on Linux](https://carla.readthedocs.io/en/0.9.13/build_linux/)（适用于 Ubuntu 18.04 及以下的所有版本）或 [Building on Windows](https://carla.readthedocs.io/en/0.9.13/build_windows/) （按照其说明构建 CARLA 0.9.13）。使用我们的 Ubuntu 20.04 Carla 安装指南（适用于 Ubuntu 20.04）。
- （可选）同样，您可以安装原始的 [Carla Scenario Runner v0.9.13 ](https://github.com/carla-simulator/scenario_runner/tree/v0.9.13) 项目，将 DReyeVR+Carla 与 Scenario Runner 集成。
  ```bash
  git clone https://github.com/carla-simulator/scenario-runner -b v0.9.13 --depth 1
  ```

(*=Carla 不再正式支持 Mac 操作系统，但我们的开发团队已能够在搭载 Apple Silicon（arm64）硬件的新 Mac 机器上构建 UE4、Carla 和 DReyeVR。 )

<br>

# DReyeVR 安装命令总结
<details>

**注意** 您需要在 Linux/Mac 上安装一个终端。在 Windows 上，您可以使用与构建 Carla 时相同的 x64 Native Tools CMD prompt。 
<summary> 显示用于安装和构建 DReyeVR 的命令行 </summary>

```bash
mkdir CarlaDReyeVR && cd CarlaDReyeVR # 在这个 "CarlaDReyeVR" 目录中做所有事

#####################################################
########### 安装我们的 UnrealEngine fork ###########
#####################################################
# Rather than https://github.com/CarlaUnreal/UnrealEngine UE4, you SHOULD clone https://github.com/HARPLab/UnrealEngine
# 但除此之外，所有的指令都是一样的。 

# Linux: https://carla.readthedocs.io/en/0.9.13/build_linux/#unreal-engine
# Windows: https://carla.readthedocs.io/en/0.9.13/build_windows/#unreal-engine

#####################################################
################### 安装 Carla ###################
#####################################################
# Linux: https://carla.readthedocs.io/en/0.9.13/build_linux/
# Windows: https://carla.readthedocs.io/en/0.9.13/build_windows/
git clone https://github.com/carla-simulator/carla -b 0.9.13 --depth 1
cd carla
./Update.sh # linux/mac
Update.bat # Windows（已经失效，需要克隆然后切换到tag 为0.9.13的提交记录）
git clone https://bitbucket.org/carla-simulator/carla-content.git
make PythonAPI && make launch # 构建最初的 Carla

#####################################################
############## 安装 DReyeVR 插件 ##############
#####################################################
# (可选) 安装 SRanipal (眼动跟踪) SRanipal plugin 
# 安装手册：https://github.com/Tomaso-Zanardi/SRanipal-Eye-Tracking-Manual/tree/main
mv /PATH/TO/SRANIPALPLUGIN/SDK/03_Unreal/Plugins/SRanipal Unreal/CarlaUE4/Plugins/ 

# (可选) 安装 LogitechWheelPlugin (steering wheel) 
# 已合并到 [hutb仓库](https://github.com/OpenHUTB/hutb/tree/hutb/Unreal/CarlaUE4/Plugins) 
git clone https://github.com/HARPLab/LogitechWheelPlugin
mv LogitechWheelPlugin/LogitechWheelPlugin Unreal/CarlaUE4/Plugins/ # 安装到 carla

cd .. # 回到主目录

#####################################################
############## 安装 scenario_runner #################
#####################################################
# (可选) while you don't NEED scenario runner, it is certainly useful from a research
git clone https://github.com/carla-simulator/scenario_runner -b v0.9.13

#####################################################
################## 安装 DReyeVR ##################
#####################################################
git clone https://github.com/HARPLab/DReyeVR
cd DReyeVR
# CARLA= 和 SR= 变量是可选的
make install CARLA=../carla SR=../scenario_runner
# 或者（最重要）
make install CARLA=../carla
make install SR=../scenario_runner

# run filesystem checks after installing
make check CARLA=../carla
cd ..

#####################################################
################## 构建所有 #########################
#####################################################
cd carla
make PythonAPI  # 再次构建 PythonAPI (和 LibCarla)
make launch     # 启动虚幻编辑器
make package    # 创建优化过的包
make check      # 运行 Carla 单元测试
```
</details>


<br>

## 简单安装
从技术上讲，上述先决条件就是您安装 DReyeVR 并获得**没有眼动追踪**和**赛车方向盘集成**的准系统 VR ego-vehicle 所需的全部条件。如果这适合您的需求，只需跳到本文档的 [安装 DReyeVR Core](Install.md#installing-dreyevr-core) 部分，并在以下位置设置以下变量：`Unreal/CarlaUE4/Source/CarlaUE4/CarlaUE4.Build.cs` 成 `false`：
```c#
/////////////////////////////////////////////////////////////
// 编辑这些变量以启用/禁用 DReyeVR 的功能
bool UseSRanipalPlugin = true;
bool UseLogitechPlugin = true;
...
/////////////////////////////////////////////////////////////
```
- 注意：仅当启用了 `UseSRanipalPlugin` 时才需要安装 SRanipal 插件，同样，仅当启用了 `UseLogitechPlugin` 时才需要安装 Logitech 插件（插件已合并到 [hutb仓库](https://github.com/OpenHUTB/hutb/tree/hutb/Unreal/CarlaUE4/Plugins) 中）。

!!! 注意
    在虚幻编辑器中运行时，需要点击工具栏中的 [`控制`](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/playing-and-simulating?application_version=4.27) （显示`弹出`）才有进入驾驶模式。每次点击`控制`都会调用 `carla\unreal\carlaue4\Source\CarlaUE4\DReyeVR\DReyeVRPawn.cpp` 文件中 `void ADReyeVRPawn::SetupPlayerInputComponent(UInputComponent *PlayerInputComponent)` 的 `Super::SetupPlayerInputComponent(PlayerInputComponent);`，每次持有棋子时都会调用一次，从而 InputComponent 不为空。 

# 安装 DReyeVR 插件
在安装 `DReyeVR` 之前，我们还需要安装依赖项：

- **SteamVR**: VR 所必需
- **SRanipal***: 眼动追踪必需（使用 HTC Vive Pro Eye），其他情况可选
- **LogitechWheelPlugin***: 罗技方向盘必需，其他可选

(* = 可选，取决于您正在寻找的功能)

## SteamVR
### **下载 Steam 和 SteamVR**

  - 您需要使用 [SteamVR](https://store.steampowered.com/app/250820/SteamVR/) 作为 VR 渲染环境，因此您应该首先下载 [Steam 客户端应用程序](https://store.steampowered.com/about/) 。

    - 在 Steam 客户端中，您可以在商店中浏览->搜索 "[SteamVR](https://store.steampowered.com/app/250820/SteamVR/)" 并下载免费安装的系统实用程序。

  <!-- - 在 Carla 编辑器中，转到`Settings->Plugins->Virtual Reality->SteamVR`并启用插件 -->
  <!-- - Note that on Linux this you may need to install it through the [Valve GitHub repo](https://github.com/ValveSoftware/SteamVR-for-Linux) -->
  <!-- - <img src = "Figures/Install/steamvr-enabled.jpg" alt="UE4DropDown" width=50%> -->
  - 您应该能够从客户端启动 SteamVR，并在小弹出窗口中访问设置并"show VR view" 
    - 确保根据您的设置和偏好校准 VR 系统！
  - 此外，我们建议在 SteamVR 设置中禁用“运动平滑”效果，以避免渲染过程中出现令人讨厌的失真伪影。

[](Figures/Install/steamvr-settings.jpg)

***
## HTC 眼动追踪插件
### **下载 `SRanipal`**
  0. *什么是 SRanipal?*
      - 我们使用 [HTC 的 SRanipal 插件](https://developer.vive.com/resources/vive-sense/sdk/vive-eye-tracking-sdk-sranipal/) 作为虚幻引擎 4 和 Vive 的眼动仪之间通信的手段。
      - 要了解有关 SRanipal 的更多信息以及**首次设置**，请参阅 HTC 开发人员 MariosBikos_HTC 撰写的 [使用 SRanipal 进行注视点渲染的指南](https://forum.vive.com/topic/7434-getting-started-with-vrs-foveated-rendering-using-htc-vive-pro-eye-unreal-engine/) 
  1. 您需要一个（免费创建）[Vive 开发者帐户](https://hub.vive.com/sso/login) 才能下载以下内容：
      - a) [`VIVE_SRanipalInstaller_1.3.2.0.msi`](https://hub.vive.com/en-US/download/VIVE_SRanipalInstaller_1.3.2.0.msi) -- 安装 Tobii 固件的可执行文件
      - b) [`SDK_v1.3.3.0.zip`](https://hub.vive.com/en-US/download/SDK-v1.3.3.0.zip) -- 包含 Unreal 插件
        - **重要**: 1.3.6.0 以上的 SRanipal 版本不受支持并会导致严重崩溃！
      - **如果上面的下载链接对您不起作用，请确保您拥有 Vive 开发者帐户！（或直接 [联系](mailto:gustavo@silvera.cloud) 我们以帮助您）**
  2. 双击 `.msi` 安装程序安装 Tobii 固件
      - 安装完成后，您应该会在“开始”菜单中看到 `SR_runtime.exe` 程序。以管理员身份启动它，您应该会在 Windows 系统托盘中看到机器人头部图标，如下所示：
      - ![SR_runtime](https://mariosbikos.com/wp-content/uploads/2020/02/image-30.png)
        - 图片来源：[MariosBikos](https://forum.htc.com/topic/7434-getting-started-with-vrs-foveated-rendering-using-htc-vive-pro-eye-unreal-engine)

### **安装 SRanipal UE4 插件**
  - 下载 `.zip` 文件后，解压后应出现类似如下的目录（相关 [链接](https://github.com/VARID-XR/VARID-plugin-unreal) ,`software/VR/*`）

 ```text
 SDK
 - 01_C/
 - 02_Unity/
 - 03_Unreal/
 - Eye_SRanipal_SDK_Guide.pdf
 - Lip_SRanipal_SDK_Guide.pdf
 ```
      
   - 然后，解压 SRanipal 虚幻插件并将 `03_Unreal/Plugins/SRanipal/` 目录复制到 Carla 安装
    
 ```bash
 # in SDK/
 cd 03_Unreal
 unzip Vive-SRanipal-Unreal-Plugin.zip # 创建 PLugins/SRanipal 目录
 # 假设 CARLA_ROOT 已定义，否则只需使用您的 Carla 路径
 cp -r Plugins/SRanipal $CARLA_ROOT/Unreal/CarlaUE4/Plugins/
 ```
      
  - 建议为实验中的每个新参与者重新校准 SRanipal 眼动仪插件。您可以进入 SteamVR 主页，点击底部菜单栏中的小图标，将眼动仪校准到头戴式耳机佩戴者。

    - ![Calibration](Figures/Install/steamvr-home.jpg)
    - 您可以查看 HTC 开发人员 MariosBikos_HTC 撰写的 [使用 SRanipal 进行注视点渲染的指南](https://forum.vive.com/topic/7434-getting-started-with-vrs-foveated-rendering-using-htc-vive-pro-eye-unreal-engine/) ，了解更多信息
***
## 罗技方向盘插件
### **安装罗技方向盘插件**
  - 这仅适用于拥有罗技方向盘/踏板驾驶装置的人。体验 VR 体验不需要此硬件（您只需使用键盘/鼠标即可），但可以大大增强沉浸感并允许进行精细的模拟控制。

    - 作为参考，我们使用了这款 [罗技 G923 赛车方向盘和踏板](https://www.logitechg.com/en-us/products/driving/driving-force-racing-wheel.html) 。
    
  - 我们将使用这个 [LogitechWheelPlugin](https://github.com/HARPLab/LogitechWheelPlugin) 与 UE4 交互并将硬件输入映射到动作。

  - 克隆 repo 并将所需文件夹移动到 Carla 插件文件夹
    
```bash
git clone https://github.com/HARPLab/LogitechWheelPlugin
mv LogitechWheelPlugin/LogitechWheelPlugin $CARLA_ROOT/Unreal/CarlaUE4/Plugins
```
      
   - 当您再次启动编辑器时，您应该会看到已启用的 Logitech 插件：
   - ![LogitechPlugin](Figures/Install/LogitechPlugin.jpg)


## 完整性检查
  - 安装这些插件后，您应该会看到如下所示的 `Unreal/CarlaUE4/Plugins`：

```
Plugins
├── Carla                              # 未改变
│   └── ...
├── CarlaExporter                      # 未改变
│   └── ...
├── LogitechWheelPlugin                # 如果已安装
│   ├── Binaries
│   ├── Doc
│   ├── Logitech
│   ├── LogitechWheelPlugin.uplugin
│   ├── Resources
│   └── Source
└── SRanipal                           # 如果已安装
    ├── Binaries
    ├── Config
    ├── Content
    ├── Resources
    ├── Source
    └── SRanipal.uplugin  
```
    
  - 如果您还有疑问或问题，请随时在我们的 [问题](https://github.com/HARPLab/DReyeVR/issues) 页面上发布问题，我们将尽力帮助您。

<br>

# 安装 `DReyeVR` 核心
<!-- (Once you are done with this step, you should have a carla repo that looks just like this [Carla fork](https://github.com/HARPLab/carla/tree/DReyeVR-0.9.13) we created with the installation (and other minor things) pre-applied.) -->

- **重要** 安装要求你的 shell 上有 `make`、`python` 和 `git`。

- 只需要安装到 `CARLA` 目录即可，ScenarioRunner是可选的。

  - 如果您不提供 `make` 变量 `CARLA=...` 或 `SR=...`，安装向导将通过查看 Carla 所需的环境变量 `CARLA_ROOT` 和 `SCENARIO_RUNNER_ROOT` 自动检测您的安装目标。 

```bash
# the CARLA= and SR= variables are optional
make install CARLA=../carla SR=../scenario_runner
# or
make install CARLA=../carla
make install SR=../scenario_runner

# run filesystem checks after installing
make check CARLA=../carla
```
**NOTE:** to learn more about how the DReyeVR `make` system works, see [`Scripts/README.md`](../Scripts/README.md)


# 构建 `DReyeVR` PythonAPI
## 对 PythonAPI 使用 [`conda`](https://www.anaconda.com/products/distribution) 
  - While not required for DReyeVR, we highly recommend compartmentalizing Python installations via isolated environments such as [`anaconda`](https://www.anaconda.com/products/distribution)
    - First download and install Anaconda to your machine from [here](https://www.anaconda.com/products/distribution).
  ```bash
  # in /PATH/TO/CARLA/
  conda create --name carla13 python=3.7.2
  conda activate carla13 # will need to run this ONCE before opening a new terminal!
  conda install numpy
  ```
- **READ THIS FIRST (Linux)**: You might run into a problem when compiling Boost 1.72.0 (required by `LibCarla`).
    <details>

    <summary> Show instructions to get Anaconda working on Linux </summary>

    - ```bash
      # find anaconda install:
      which python3
      ... PATH/TO/ANACONDA/envs/carla/bin/python3 # example output

      # go to carla/install dir from here
      cd PATH/TO/ANACONDA/envs/carla/include

      # create a symlink between python3.7 -> python3.7m
      ln -s python3.7m python3.7
      ```
      Install `boost_1_72_0.tar.gz` manually from https://github.com/jerry73204/carla/releases/tag/fix-boost and place file in `Build/boost_1_72_0.tar.gz`
      Open `Util/BuildTools/Setup.sh` (or `Util/BuildTools/Setup.bat` on Windows)
      Find the section named `Get boost` includes and comment out the `wget` lines.
      Now when you `make LibCarla` again, the `boost` errors should be resolved.
      - For more information see the bottom of this [SO post](https://stackoverflow.com/questions/42839382/failing-to-install-boost-in-python-pyconfig-h-not-found)
    </details>

  - **READ THIS FIRST (Windows)**: Windows anaconda is a bit more of a pain to deal with.
    <details>

    <summary> Show instructions to get Anaconda working on Windows </summary>

      1. Enable your environment
          ```bat
          conda activate carla13
          ```
      2. Add carla to "path" to locate the PythonAPI and ScenarioRunner. But since Anaconda [does not use the traditional `PYTHONPATH`](https://stackoverflow.com/questions/37006114/anaconda-permanently-include-external-packages-like-in-pythonpath) you'll need to:
          - 3.1. Create a file `carla.pth` in `\PATH\TO\ANACONDA\envs\carla\Lib\site-packages\`
          - 3.2. Insert the following content into `carla.pth`:
            ```bat
              C:\PATH\TO\CARLA\PythonAPI\carla\dist
              C:\PATH\TO\CARLA\PythonAPI\carla\agents
              C:\PATH\TO\CARLA\PythonAPI\carla
              C:\PATH\TO\CARLA\PythonAPI
              C:\PATH\TO\CARLA\PythonAPI\examples
              C:\PATH\TO\SCENARIO_RUNNER\
            ```
      3. Install the specific carla wheel (`whl`) to Anaconda
          ```bash
          conda activate carla13
          pip install --no-deps --force-reinstall PATH\TO\CARLA\PythonAPI\carla\dist\carla-0.9.13-cp37-cp37m-win_amd64.whl

          # if applicable (and you installed Scenario runner)
          cd %SCENARIO_RUNNER_ROOT%
          pip install -r requirements.txt # install all SR dependencies
          ```
      4. Finally, you might run into problems with `shapely` (scenario-runner dependency) and Conda. Luckily the solution is simple:
          - Copy the files:
            - `PATH\TO\ANACONDA\envs\carla13\Lib\site-packages\shapely\DLLs\geos.dll`
            - `PATH\TO\ANACONDA\envs\carla13\Lib\site-packages\shapely\DLLs\geos_c.dll`
          - To destination:
            - `PATH\TO\ANACONDA\envs\carla13\Library\bin\`
      5. Now finally, you should be able to verify all PythonAPI actions work as expected via:
          ```bat
          conda activate carla13
          python
          >>> Python 3.7.2 (default, Feb 21 2019, 17:35:59) [MSC v.1915 64 bit (AMD64)] :: Anaconda, Inc. on win32
          >>> Type "help", "copyright", "credits" or "license" for more information.
          >>> import carla
          >>> from DReyeVR_utils import find_ego_vehicle
          >>> from scenario_runner import ScenarioRunner
          ```
          With all these imports passing (no error/warning messages), you're good to go!
        
  </details>

Now you can finally build the PythonAPI to this isolated conda environment. 
  ```bash
  conda activate carla13
  (carla13) make PythonAPI # builds LibCarla and PythonAPI to your (conda) python environment
  ```
  - NOTE: You'll need to run `conda activate carla13` every time you open a new terminal if you want to build DReyeVR since the shell needs to know which python environment to use. Luckily this minor inconvenience saves us from the significant headaches that arise when dealing with multiple `python` projects, Carla installations, and versions, etc. 

## Sanity Check:

It is nice to verify that the Carla PythonAPI is correctly visible in conda, to do this you should see all the following attributes in the `carla` module once calling `dir` on it.

<details>
<summary>Show instructions to verify Carla PythonAPI is installed </summary>

```bash
# in your terminal (linux) or cmd (Windows)
conda activate carla13   # (if using conda)
(carla13) python         # should default to python3!!
```

```python
#in Python
...
>>> import carla
>>> dir(carla)
# the following output means carla is not correctly installed :(
>>> ['__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__']

# OR the following output means carla is installed :)
>>> ['Actor', 'ActorAttribute', 'ActorAttributeType', 'ActorBlueprint', 'ActorList', 'ActorSnapshot', 'ActorState', 'AttachmentType', 'BlueprintLibrary', 'BoundingBox', 'CityObjectLabel', 'Client', 'ClientSideSensor', 'CollisionEvent', 'Color', 'ColorConverter', 'DReyeVREvent', 'DVSEvent', 'DVSEventArray', 'DebugHelper', 'EnvironmentObject', 'FakeImage', 'FloatColor', 'GearPhysicsControl', 'GeoLocation', 'GnssMeasurement', 'IMUMeasurement', 'Image', 'Junction', 'LabelledPoint', 'Landmark', 'LandmarkOrientation', 'LandmarkType', 'LaneChange', 'LaneInvasionEvent', 'LaneInvasionSensor', 'LaneMarking', 'LaneMarkingColor', 'LaneMarkingType', 'LaneType', 'LidarDetection', 'LidarMeasurement', 'Light', 'LightGroup', 'LightManager', 'LightState', 'Location', 'Map', 'MapLayer', 'MaterialParameter', 'ObstacleDetectionEvent', 'OpendriveGenerationParameters', 'OpticalFlowImage', 'OpticalFlowPixel', 'Osm2Odr', 'Osm2OdrSettings', 'RadarDetection', 'RadarMeasurement', 'Rotation', 'SemanticLidarDetection', 'SemanticLidarMeasurement', 'Sensor', 'SensorData', 'ServerSideSensor', 'TextureColor', 'TextureFloatColor', 'Timestamp', 'TrafficLight', 'TrafficLightState', 'TrafficManager', 'TrafficSign', 'Transform', 'Vector2D', 'Vector3D', 'Vehicle', 'VehicleControl', 'VehicleDoor', 'VehicleLightState', 'VehiclePhysicsControl', 'VehicleWheelLocation', 'Walker', 'WalkerAIController', 'WalkerBoneControlIn', 'WalkerBoneControlOut', 'WalkerControl', 'Waypoint', 'WeatherParameters', 'WheelPhysicsControl', 'World', 'WorldSettings', 'WorldSnapshot', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'bone_transform', 'bone_transform_out', 'command', 'libcarla', 'vector_of_bones', 'vector_of_bones_out', 'vector_of_gears', 'vector_of_ints', 'vector_of_transform', 'vector_of_vector2D', 'vector_of_wheels']
```
</details>

<br>

## Future modifications

Additionally, if you make changes to the `PythonAPI` source and need to rebuild (`make PythonAPI` again) when using Conda you should reinstall the `.whl` file to ensure your changes will be reflected in the environment:
  - ```bash
    conda activate carla

    pip install --no-deps --force-reinstall /PATH/TO/CARLA/PythonAPI/carla/dist/carla-YOUR_VERSION.whl
    ```


# 升级 `DReyeVR`
If you currently have an older version of `DReyeVR` installed and want to upgrade to a newer version, it is best to re-install DReyeVR from a fresh Carla repository. You can manually delete the `carla` repository and re-clone it directly (carefully ensuring the versions match) or use our provided scripts which attempt to reset the repository for you:

<details>
<summary> Show instructions to use DReyeVR scripts to reset CARLA repo</summary>

**IMPORTANT:** the `DReyeVR` clean script will overwrite and reset the Carla repository you specify, so make your backups now if you have any unstaged code. (`git reset --hard HEAD` and `git clean -fd` will be invoked, so if you commit your local changes they will be safe)

```bash
# first go to CARLA and clean it so no old DReyeVR builds linger
cd /PATH/TO/Carla/
make clean

# it is a good idea to clean the Content/ directory which is not tracked by Carla's git system
rm -rf Unreal/CarlaUE4/Content/

# re-install the Content fresh from Carla's servers
./Update.sh # Linux/Mac
Update.bat  # Windows

# next, go to DReyeVR and get the latest updates
cd /PATH/TO/DReyeVR/
git pull origin main # or dev, or whatever branch

# next, run the DReyeVR-cleaner to automatically hard-reset the Carla repo
# accept the prompt to hard-clean CARLA, note that this will reset tracked and remove untracked files
make clean CARLA=/PATH/TO/CARLA SR=/PATH/TO/SR # both args are optional

# now, you can cleanly install DReyeVR over Carla again
make install CARLA=/PATH/TO/CARLA SR=/PATH/TO/SR # both args are optional

# it's a good idea to check that the Carla repository has all the expected files
make check CARLA=/PATH/TO/CARLA SR=/PATH/TO/SR # both args are optional

# finally, you can go back to Carla and rebuild
cd /PATH/TO/Carla
make PythonAPI
make launch
make package
```

***

As long as you have no errors in the previous sections, you should be able to just build the `Carla` project with our `DReyeVR` files as follows:

</details>

<br>
<br>

# 构建 `DReyeVR` UE4
如果您不想使用 SRanipal 或 LogitechWheelPlugin，您可以在编译时通过将 `Unreal/CarlaUE4/Source/CarlaUE4/CarlaUE4.Build.cs` 中的变量更改为 `false` 来禁用它们：
```c#
  /////////////////////////////////////////////////////////////
  // 编辑这些变量以启用/禁用 DReyeVR 的功能
  bool UseSRanipalPlugin = true;
  bool UseLogitechPlugin = true;
  ...
  /////////////////////////////////////////////////////////////
  ```

最后，在任何终端（Linux / Mac）或 VS 2019 的 `Windows x64 Native Tools Command Prompt for VS 2019`（Windows）中打开项目目录并运行：
```bash
make PythonAPI  # 构建 PythonAPI & LibCarla

make launch     # 在编辑器中构建 development UE4 game

make package    # 构建优化的 UE4 打包游戏（打包）
```

# 运行 `DReyeVR`

构建运输 shipping 包后，在 VR 模式下运行 Carla（安装了 DReyeVR）可执行文件：
```bash
# on Unix
cd /PATH/TO/CARLA/Dist/CARLA_Shipping_0.9.13-dirty/LinuxNoEditor/ # or MacNoEditor on MacOS
./CarlaUE4.sh -vr

# on Windows x64 Visual C++ Toolset
cd \PATH\TO\CARLA\Build\UE4Carla\0.9.13-dirty\WindowsNoEditor\
CarlaUE4.exe -vr

# Optional flag: -quality-level=Low
```
**注意：** 为了在不损失太多视觉保真度的情况下大幅提高帧速率，您可以使用附加参数 `-quality-level=Low` 运行，我们从 vanilla Carla 对其进行了修改，以保持相同的渲染距离。

**注意 2** 您也不一定需要在 VR 中运行 DReyeVR。如果您省略 `-vr` 标志，那么您将看到一款平板 Carla 游戏，该游戏具有 DReyeVR 的相同功能，只是不在 VR 中。

<br>

# 现在该怎么办？

现在您已成功安装 DReyeVR，请继续访问 [`Usage.md`](Usage.md) 了解如何将 DReyeVR 用于您自己的 VR 驾驶研究模拟器。

VR模式和传统模型进行切换需要修改`Unreal/CarlaUE4/Config/DefaultEngine.ini`文件中的`GlobalDefaultGameMode`配置。传统模式：
```shell
[/Script/EngineSettings.GameMapsSettings]
EditorStartupMap=/Game/Carla/Maps/Town10HD_Opt.Town10HD_Opt
GameDefaultMap=/Game/Carla/Maps/Town10HD_Opt.Town10HD_Opt
ServerDefaultMap=/Game/Carla/Maps/Town10HD_Opt.Town10HD_Opt
GlobalDefaultGameMode=/Game/Carla/Blueprints/Game/CarlaGameMode.CarlaGameMode_C
GameInstanceClass=/Script/Carla.CarlaGameInstance
TransitionMap=/Game/Carla/Maps/Town10HD_Opt.Town10HD_Opt
GlobalDefaultServerGameMode=/Game/Carla/Blueprints/Game/CarlaGameMode.CarlaGameMode_C
```
VR模式（默认启动的地图是Town03，）：
```shell
[/Script/EngineSettings.GameMapsSettings]
EditorStartupMap=/Game/Carla/Maps/Town03.Town03
LocalMapOptions=
TransitionMap=/Game/Carla/Maps/Town03.Town03
bUseSplitscreen=True
TwoPlayerSplitscreenLayout=Horizontal
ThreePlayerSplitscreenLayout=FavorTop
FourPlayerSplitscreenLayout=Grid
bOffsetPlayerGamepadIds=False
GameInstanceClass=/Script/Carla.CarlaGameInstance
GlobalDefaultGameMode=/Script/CarlaUE4.DReyeVRGameMode
GlobalDefaultServerGameMode=/Script/CarlaUE4.DReyeVRGameMode
```



