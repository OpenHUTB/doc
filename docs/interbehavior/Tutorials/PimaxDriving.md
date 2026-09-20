# Pimax Dream Air 驾驶与眼动追踪

本页介绍如何在 OpenHUTB（DReyeVR）中使用 Pimax Dream Air 系列头显和 Crystal 手柄，包括手柄驾驶、连续调整座椅、combined gaze 眼动追踪以及蓝色注视线显示。

手柄功能适用于 Pimax SteamVR 驱动识别为 `oculus_touch` 的设备；眼动追踪目前已在 **Pimax Dream Air + Windows + Pimax Play + SteamVR** 环境中完成实机验证。

对应代码改动：

- [Pimax 手柄驾驶与座椅连续移动 OpenHUTB/hutb#3665](https://github.com/OpenHUTB/hutb/pull/3665)
- [Pimax 眼动追踪与相机附着视线 OpenHUTB/hutb#3670](https://github.com/OpenHUTB/hutb/pull/3670)

## 功能状态

| 功能 | Dream Air 验证状态 |
| --- | --- |
| VR 显示与头部追踪 | ✓ |
| 左摇杆转向、扳机油门/刹车、A 键换挡 | ✓ |
| 右摇杆连续调整座椅前后/左右 | ✓ |
| 左右握把连续降低/升高座椅 | ✓ |
| combined gaze 眼动方向 | ✓ |
| 蓝色注视线、焦点检测、录制及 Python API 数据链 | ✓ |
| 单眼原点、瞳孔直径、眼睛开合度 | PVR 1.26 接口未提供 |

## 效果预览

静止注视：车辆停止时，蓝色视线随眼球移动并指向道路左前方目标。

![Dream Air 静止眼动追踪](../Figures/PimaxEyeTracking_Static.jpg)

行驶跟随：车辆行驶时，蓝色视线保持附着于头显相机，不会落在车辆后方（仪表速度单位取决于车辆配置）。

![Dream Air 行驶中眼动追踪](../Figures/PimaxEyeTracking_Driving.jpg)

注视转移：车辆继续行驶时，视线能够转向道路右侧目标，展示 combined gaze 的连续变化。

![Dream Air 行驶中转移注视点](../Figures/PimaxEyeTracking_GazeShift.jpg)

下面的视频为 Dream Air 实机内录。蓝色注视线的起点固定在头显前方，终点随眼球注视方向移动；车辆行驶时，视线会跟随相机，不会落在车辆后方。

<video controls playsinline width="100%" preload="metadata" poster="/doc/interbehavior/Figures/PimaxDreamAir_EyeTracking_Poster.jpg">
  <source src="/doc/interbehavior/Videos/PimaxDreamAir_EyeTracking.mp4" type="video/mp4">
  当前浏览器不支持内嵌视频，请使用下方链接观看。
</video>

[下载或单独观看 Pimax Dream Air 眼动追踪演示](../Videos/PimaxDreamAir_EyeTracking.mp4)

设备图样：Pimax Dream Air 头显与 Crystal 手柄置于桌面，显示器同步输出旁观画面，红字 `0 R` 表示当前车速 0、倒挡。

![设备图样](../Figures/PimaxDriving_Setup.jpg)

手柄驾驶：显示器为座舱视角，方向盘随左摇杆实时转动，红字 `33 D` 表示车速读数 33、前进挡。

![手柄驾驶](../Figures/PimaxDriving_Driving.jpg)

## 工作原理

### 手柄输入

Pimax 的 SteamVR 驱动（aapvr）会把 Crystal 手柄上报为 `oculus_touch`。OpenHUTB 使用 SteamVR action 将手柄输入传递给 DReyeVR：

- `CarlaUE4/Config/SteamVRBindings/steamvr_manifest.json`：声明转向、油门、刹车、换挡和座椅调整 action；
- `CarlaUE4/Config/SteamVRBindings/oculus_touch.json`：将 Crystal 手柄按键映射到 action；
- `CarlaUE4/Config/DefaultInput.ini`：将 SteamVR action 绑定到 DReyeVR 输入；
- 右摇杆使用标准 `vector2 position`，座椅移动使用 15% 死区并按帧时间计算，避免松开摇杆后漂移或不同帧率下速度不一致。

### 眼动追踪

Pimax 眼动后端在 Windows 上运行时加载 `libPVRClient64.dll`，因此编译 OpenHUTB 时不需要安装 Pimax SDK，也不会随项目分发 Pimax 二进制文件。

#### DLL 的来源与另一台电脑的使用条件

`libPVRClient64.dll` 是**小派官方编译、由 Pimax Play 安装程序提供**的运行库，不是本项目编写的 DLL，也不是我们的程序在使用时生成的文件。原代码中的 `C:\Windows\System32\libPVRClient64.dll` 和 `C:\Program Files\Pimax\Runtime\libPVRClient64.dll` 是**同一个 DLL 的两个候选位置**，并非必须同时存在的两个依赖。

不能只把 DLL 复制给其他用户：它还依赖 Pimax Play 安装的驱动、Pimax Runtime 和眼动服务。仓库不重新分发这一官方二进制文件。另一台电脑需要安装 **Pimax Play + SteamVR**，开启并校准眼动，使用包含本次代码的已编译程序。仅下载 GitHub 源码并不等于获得可直接运行的程序；旧的打包版本也不会自动包含新功能。

新版后端不再假设 Windows 或 Pimax 安装在 C 盘，按以下顺序寻找运行库：

1. 若设置了 `PIMAX_PVR_DLL`，只使用该本地绝对路径；路径错误时明确报错，不悄悄换用其他版本；
2. Windows 实际系统目录中的 `libPVRClient64.dll`；
3. 注册表登记的 Pimax/PiTool 安装目录下的 `Runtime\libPVRClient64.dll` 或 `libPVRClient64.dll`；
4. 系统 Program Files 下的默认 Pimax 安装目录。

不会从当前工作目录或 `PATH` 随意加载同名 DLL。自定义安装路径仍找不到时，可在启动脚本中指定 `-PimaxRoot 'E:\VR\Pimax'`，或指定 `-PvrDllPath 'E:\VR\Pimax\Runtime\libPVRClient64.dll'`。应指向**官方安装的文件**，不要下载来源不明的 DLL。

后端通过 PVR 1.26 接口读取 combined gaze，将方向转换为 Unreal Engine 坐标系，并接入 DReyeVR 原有的注视射线、目标检测、记录器和 Python API。读取过程中会检查设备状态、时间戳、有限值、可信范围和数据新鲜度；设备断开或读取失败后会自动重连。

### 蓝色注视线

蓝色注视线作为组件附着于 VR 相机：

- 起点固定在头显前约 30 cm；
- 眼球移动只改变射线方向和终点；
- 在相机姿态更新后刷新，避免车辆行驶时射线落后；
- 样本无效、过期或时间戳为 0 时自动隐藏。

该显示方式只影响调试视线，不改变记录器或 Python API 中的眼动数据。

## 使用前准备

1. 安装并启动 Pimax Play，连接 Dream Air 和 Crystal 手柄；
2. 在 Pimax Play 中开启眼动追踪并完成眼动校准；
3. 从 Steam 安装 SteamVR，首次手动运行一次并确认头显和手柄正常连接；之后可由启动脚本自动拉起；
4. 使用包含 [OpenHUTB/hutb#3670](https://github.com/OpenHUTB/hutb/pull/3670) 的版本；
5. 建议先关闭不需要的高开销功能，例如三个实时后视镜。

## 配置

在 `Unreal/CarlaUE4/Config/DReyeVRConfig.ini` 中确认以下配置：

```ini
[CameraParams]
SeatMoveSpeedCmPerSecond=75.0

[EgoSensor]
DrawDebugFocusTrace=True
UseCameraRelativeGazeDisplay=True

[Pimax]
EnablePvrEyeTracking=True
AllowUnknownPimaxDevice=False
AllowedVendorIds=0x34A4
AllowedProductIds=0x0012,0x0040,0x0042,0x0044
MaxSampleAgeSeconds=0.5
GazeInvertHorizontal=False
GazeInvertVertical=False
```

其中 `0x0044` 为本次实测 Dream Air 的产品 ID。若后续验证其他 Pimax 型号，应确认其 VID/PID 后再加入白名单，不建议长期使用 `AllowUnknownPimaxDevice=True`。

## 启动方法

### 推荐：带检查的启动脚本

在**新版打包程序的根目录**打开 64 位 Windows PowerShell，执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\StartPimaxVR.ps1
```

`Bypass` 只对这次 PowerShell 进程生效，不会永久修改系统执行策略。默认地图为 Town02；若安装了其他地图，可添加 `-Map /Game/Carla/Maps/Town10HD_Opt`。打包时必须已包含所选地图。

**源码开发版**需要先编译引擎和 `CarlaUE4Editor Win64 Development`，然后在源码根目录执行（引擎路径按实际位置修改）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\StartPimaxVR.ps1 -UE4Root 'H:\hutb-dev\UE4-hutb' -Map /Game/Carla/Maps/Town10HD_Opt
```

脚本会检查程序、SteamVR 插件启用配置、眼动与蓝色视线开关、Dream Air 设备白名单、座椅 action 绑定、官方 DLL 和 SteamVR 安装位置。之后启动尚未运行的 Pimax Play、SteamVR，等待 `vrserver` 和 `vrcompositor` 进程出现，再启动游戏；超时则提示排查，不继续启动游戏。它不会修改系统全局环境变量或替你打开/校准眼动。

只检查、不启动任何程序时，在上述命令末尾添加 `-CheckOnly`。SteamVR 路径未登记时可指定 `-SteamVRRoot 'D:\steam\steamapps\common\SteamVR'`。

**注意：** SteamVR 必须在 `CarlaUE4.uproject` 中启用后再编译/打包；脚本不能让缺少 VR 插件的旧二进制程序具备 VR 功能。新版 `Util/BuildTools/Package.bat` 会把启动脚本、项目描述文件、DReyeVR 配置和 SteamVR 绑定放进安装包，不打包 Pimax DLL。仅替换启动脚本不等于升级整个安装包。

### 手动启动与成功判据

已手动启动 Pimax Play 和 SteamVR 时，打包版的实际游戏命令为：

```powershell
.\CarlaUE4.exe /Game/Carla/Maps/Town02?game=/Script/CarlaUE4.DReyeVRGameMode -game -vr
```

这里直接指定 DReyeVR 游戏模式，不依赖某台电脑额外配置的 `GAME=VR` 别名。手动命令本身**不包含**上述启动检查和自动拉起 SteamVR 的功能。

戴上头显，确认显示和手柄正常，并在游戏日志中检查：

```text
Using Pimax PVR eye tracking
Pimax PVR: first valid eye sample
```

这些日志、持续更新的样本和随注视移动的蓝色视线共同用于确认数据链正常。启动脚本检查通过或 SteamVR 进程存在，**不能单独证明**头显有画面或眼动服务已开始出数。

## 自动测试（不需要连接头显）

以下为开发者回归测试，不是给普通驾驶用户增加的使用步骤。需要 Windows 上已编译的引擎、项目 Editor 模块及项目资源；纯逻辑测试不需要安装 Pimax SDK、不需要 Pimax DLL 或连接头显。

在**源码根目录**执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Util\Tests\RunPimaxTests.ps1 -UE4Root 'H:\hutb-dev\UE4-hutb'
```

脚本使用 `UE4Editor-Cmd.exe`、`-NullRHI -nohmd` 和 `Automation RunTests HUTB.Pimax`，在无头显、无图形渲染模式下运行以下 5 项测试（原有 4 项加上运行库路径测试）：

| 测试名称 | 检查内容 |
| --- | --- |
| `HUTB.Pimax.EyeTracking.Freshness` | 眼动样本时间戳与新鲜度判断 |
| `HUTB.Pimax.GazeDisplay.CameraAttachment` | 调试视线附着于相机及更新依赖 |
| `HUTB.Pimax.GazeDisplay.FixedAnchor` | 视线起点固定、终点跟随注视方向 |
| `HUTB.Pimax.SeatInput.DeadZone` | 座椅输入死区与连续移动计算 |
| `HUTB.Pimax.Runtime.DiscoveryPaths` | 非 C 盘系统、自定义安装路径、去重及拒绝相对路径覆盖 |

默认报告保存在 `Unreal/CarlaUE4/Saved/Automation/Pimax-时间戳/`，包括 `index.json` 和 `automation.log`；也可通过 `-ReportPath 'D:\HUTB-test\run-001'` 指定**尚不存在**的目录，避免误读旧结果。脚本要求上述 5 项均为 `Success`，没有失败或未运行项目才输出 `PASS`；退出码为 0 表示通过，非 0 表示失败或运行异常。运行超过 10 分钟会停止本次测试进程并报错。

启动脚本另外提供 7 项轻量隔离测试，只需 Windows PowerShell 5.1，无需 UE4、Pimax Play 或 SteamVR：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Util\Tests\TestPimaxLauncher.ps1
```

它使用临时目录和模拟的进程调用，检查带空格的安装路径、只检查不启动、Pimax Play → SteamVR → 游戏的启动顺序与 VR 参数、环境变量恢复，以及插件关闭、眼动关闭、旧绑定、DLL 缺失和相对 DLL 路径的拦截。它不会真的启动软件或连接设备。

这些测试不验证真实 DLL 的加载、SteamVR 显示、硬件眼动出数或打包完整性。发布前仍需在装有 Pimax Play 和 SteamVR 的另一台电脑上检查启动、眼动校准、行驶中注视线、手柄和设备断连恢复。目前已验证开发机编译与逻辑测试；新启动流程和新打包流程不应描述为已经通过第二台电脑实测。

后续可以在具备 UE4 与项目资源的 Windows CI 运行机上调用同一脚本，并保存报告目录；本次不宣称已经配置了 GitHub Actions 硬件测试。

## 手柄键位

| 功能 | 操作 |
| --- | --- |
| 转向（比例） | 左摇杆左右 |
| 油门（比例） | 右手扳机 |
| 刹车（比例） | 左手扳机 |
| 倒挡/前进挡切换 | A |
| 左转向灯 | X |
| 右转向灯 | B |
| 下一个摄像机视角 | Y |
| 上一个摄像机视角 | 右摇杆按下 |
| 自车/旁观视角切换 | 左摇杆按下 |
| 座椅升高 / 降低 | 右手柄握把 / 左手柄握把 |
| 座椅前后左右移动 | 右摇杆四向 |

## 常见问题

### 能识别设备，但没有眼动数据

如果日志持续出现 `timestamp-zero`，或者没有 `first valid eye sample`：

1. 退出模拟器；
2. 在 Pimax Play 中确认眼动追踪开关已开启；
3. 重新运行一次眼动校准；
4. 若仍无数据，重启 Pimax Play 或 Pimax 眼动运行时；
5. 确认眼动数据恢复后再启动模拟器。

时间戳为 0 时，后端会拒绝该样本，避免用无效数据绘制或录制视线。

### 有眼动数据，但看不到蓝色视线

确认 `DrawDebugFocusTrace=True` 和 `UseCameraRelativeGazeDisplay=True`，修改配置后重新启动模拟器。还应检查样本是否因时间戳停止更新而被判定为过期。

### 视线方向左右或上下相反

完成眼动校准后再测试。如坐标方向仍然相反，可分别调整：

```ini
GazeInvertHorizontal=True
GazeInvertVertical=True
```

只修改实际相反的轴。

### 右摇杆无法连续调整座椅

确认 SteamVR 使用当前应用的 Pimax/`oculus_touch` 绑定，并检查右摇杆是否绑定到标准 `vector2 position` action。旧的 `joystick::x/y` 或 dpad 绑定可能导致输入静默失效。

### 注视后视镜时严重掉帧

DReyeVR 的三个后视镜会额外渲染场景，VR 中开销较高。测试眼动追踪时可在车辆配置中暂时关闭：

```ini
RearMirrorEnabled=False
LeftMirrorEnabled=False
RightMirrorEnabled=False
```

这是性能选项，不是 Pimax 眼动功能的必要条件。

## 已知限制

- 眼动后端目前只在 Windows 和 Pimax Dream Air 上完成实机验证；
- PVR 1.26 当前只提供 combined gaze 和设备时间戳，单眼原点、瞳孔直径和眼睛开合度保持无效状态；
- Pimax Runtime 更新 ABI 或安装位置后，可能需要同步更新后端；
- SRanipal 和 Pimax 眼动后端同时开启时，DReyeVR 优先使用 SRanipal；
- Dream Air 初始视角位置偏高的问题不属于本次适配范围。
