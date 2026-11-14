# 驾驶学习启动器和数据记录

## 快速开始

1. 连接头显，在 Pimax Play 中启用眼动追踪，并完成校准。使用 Logitech G29 / G920 / G923 赛车方向盘时，确认 Logitech G HUB 已检测到方向盘，并且在 Windows 的 `joy.cpl` 中方向盘和踏板轴有响应，然后关闭测试对话框。
2. 在仓库或包的根目录中双击 `StartDrivingStudy.cmd`。
3. 选择 **Pimax Controller** 或**Logitech Racing Wheel**（Logitech 赛车方向盘）。在源代码签出状态下，输入 UE4 引擎根目录；已安装的地图和自车配置会自动从项目中发现。

4. 要记录一次试验，请勾选**Record driving data**（记录驾驶数据）。默认的目标频率是 **120 Hz**（轻量级课堂课程设置为 **20 Hz**），并输入或选择参与者ID和输出目录。可选开关：

      - **记录视口截图**（默认 **20 Hz**，640x480 JPEG；可选勾选 **Async screenshots**（异步截图），这样 GPU 读取和 JPEG 编码就不会阻塞游戏线程）。
      - **120 Hz 眼动追踪线程**（在专用后台线程上轮询眼动追踪器，并以 120 Hz 运行在线 I-VT 眼跳检测器）。
      - **记录控制器姿势**（可选择加入；为两个控制器附加 18 个手部姿势列，供下面的上肢肌肉骨骼回放使用）。
      - **渲染质量降级**（明确设置 `sg.ShadowQuality 0`，`sg.EffectsQuality 0`，`sg.PostProcessQuality 0`；默认关闭，所以正常启动会保留现有的可扩展性设置）。 
   
5. 点击**Check Settings**（检查设置），然后在预检成功后点击**Start VR**（启动 VR）。启动程序将依次启动 Pimax Play、SteamVR 和模拟器。 
6. 使用赛车方向盘驾驶时，在开始试验之前，先按下并松开油门和刹车踏板一次，以校准踏板行程。退出模拟器后，点击**Open Data Directory**（打开数据目录）以查看生成的 CSV 文件。

默认情况下录制是关闭的。每次录制运行都会生成一个新的 `<session>.csv`（71 列，启用手部姿势时为 89 列）和 `<session>_gaze.csv`（18 列），且不会覆盖之前的会话。默认输出根目录为源代码构建中的 `Unreal/CarlaUE4/Saved/DrivingStudy/`，或打包构建中的 `CarlaUE4/Saved/DrivingStudy/`；当提供有效的参与者名称并启用录制或截图时，文件将放置在 `<OutputDir>/<Participant>/` 下。重新加载地图或重新生成自车会启动一个新的会话文件。

当选择赛车方向盘输入模式时，VR 控制器和键盘将不再控制方向、油门、刹车、换挡或转向信号（控制器仍可调整摄像头/座椅姿态）。当选择控制器输入模式时，赛车方向盘的驾驶轴将被忽略，标准键盘快捷键仍可使用。如果在方向盘模式下方向盘断开或读取失败，将施加全刹车，并每两秒尝试重新连接一次。

如果方向盘没有反应，请检查 `Unreal/CarlaUE4/Saved/Logs/CarlaUE4.log`：
- `Logitech SDK initialize: success` 表示 DirectInput/Logitech SDK 已初始化。
- `Found Logitech wheel` 表示已打开受支持的轮设备。
- `Logitech wheel sample` 每两秒记录一次原始的转向和踏板数值。

也支持命令行启动：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\StartPimaxVR.ps1 -UE4Root '<UE4 source engine root>' -Map /Game/Carla/Maps/Town10HD_Opt -InputDevice wheel -RecordDriving -RecordHz 120 -EyeThreadHz 120
```

- 在 VR 控制器模式下使用 `-InputDevice controller`；当不需要录制时，省略 `-RecordDriving`。 
- 使用 `-RecordHz 20` 可进行轻量级 20 Hz 记录，或使用 `-RecordDirectory <local absolute path>` 自定义输出目录。
- 可选标志：`-ScreenshotDriving -ScreenshotHz 20` (单独使用时也会遵循 `-RecordDirectory`), `-AsyncScreenshot`, `-EyeThreadHz 120`, `-HandPose`, 以及 `-PerfDowngrade`。

从源代码构建需要在 `CarlaUE4.uproject` 中启用 `LogitechWheelPlugin` 和 `SteamVR`。


## CSV 概述

### 1. 主驾驶表 `<session>.csv` (71 列，手部姿势有 89 列)

每一行代表一个游戏线程样本，结合了当前的眼动跟踪状态、焦点射线命中、头部姿态、实时扫视指标、车辆运动学、控制输入、OpenDRIVE 道路位置以及影响交通灯状态。


| 列 | 描述 |
| --- | --- |
| `schema_version` | CSV 概述版本（`3`；在手势列存在之前是 `2`） |
| `ue_frame`, `sim_time_s`, `host_elapsed_s` | 虚幻帧数，模拟时间戳（秒），从录制开始到现在的实时时间（秒） |
| `eye_device_timestamp_ms` | 眼动追踪设备时间戳（毫秒）；使用的是设备时钟而不是模拟时间 |
| `input_mode`, `wheel_connected`, `autopilot` | 所选输入模式（`controller` 控制器 / `wheel` 方向盘）、方向盘连接状态、自动驾驶状态 |
| `map`, `vehicle_id` | 地图名称及自车 CARLA Actor ID |
| `road_id`, `lane_id`, `road_s_m` | OpenDRIVE 道路 ID、车道 ID 及纵向 `s` 坐标（米） |
| `junction_id`, `in_junction` | OpenDRIVE 路口 ID 及路口标志（`1`/`0`）；若位于道路外，则为空 |
| `motion`, `yaw_rate_deg_s` | 运动标签（停止`stopped`、直行`straight`、左转`left`、右转`right`；第一行未知`unknown`）及横摆角速度（度/秒） |
| `red_light_stop_candidate` | 当相关的交通信号灯为红灯且车辆速度低于 1 km/h 时（仅作筛选辅助，而非因果证明）为 `1`  |
| `traffic_light_id`, `traffic_light_state`, `traffic_light_distance_m` | 涉及交通信号灯的 ID、状态及与灯杆的距离（米）；在信号灯触发区域外，其状态可能未知 `unknown`。 |
| `vehicle_x_m`, `vehicle_y_m`, `vehicle_z_m`, `vehicle_yaw_deg`, `speed_kmh` | 自车世界坐标位置 (m)、航向角 (deg) 及速度 (km/h)  |
| `steer_input`, `throttle_input`, `brake_input` | 当前帧的控制输入（转向`steer`在 `[-1, 1]` 范围内，油门`throttle`/制动`brake`在 `[0, 1]` 范围内；已进行输入缩放处理）  |
| `previous_applied_steer`, `previous_applied_throttle`, `previous_applied_brake`, `previous_reverse` | 在当前帧的输入被清空之前，控制数值及倒档状态已应用于车辆。  |
| `eye_source`, `gaze_valid` | 眼动追踪后端（`pimax_pvr`、`sranipal`、`dummy` 等）及有效性标志（`1`/`0`；`dummy` 始终被标记为无效）   |
| `gaze_origin_x_m`, `gaze_origin_y_m`, `gaze_origin_z_m`, `gaze_dir_x`, `gaze_dir_y`, `gaze_dir_z` | 世界空间视线射线起点（米）及单位方向向量 |
| `gaze_local_x`, `gaze_local_y`, `gaze_local_z` | 相机坐标系下的注视方向向量（将眼球转动与头部转动区分开来）  |
| `focus_hit`, `focus_actor_id`, `focus_actor_name`, `focus_kind` | 视线射线是否击中某个对象（`1`/`0`），以及该对象的 ID、名称和语义类型  |
| `focus_x_m`, `focus_y_m`, `focus_z_m`, `focus_distance_m` | 世界坐标系下的命中位置与距离（米）；当 `focus_hit=0` 时为空 |
| `focus_traffic_light_state`, `looking_at_affecting_light` | 所关注交通灯的状态，以及该交通灯是否为施加影响的交通灯（`1`/`0`） |
| `head_x_m`, `head_y_m`, `head_z_m`, `head_pitch_deg`, `head_yaw_deg`, `head_roll_deg` | 世界空间中头显摄像机的位置（米）与朝向（度） |
| `gaze_h_deg`, `gaze_v_deg` | 水平（`atan2(Y, X)`）与垂直（`atan2(Z, sqrt(X^2+Y^2))`）视线角度（度）的组合  |
| `focus_actor_yaw_deg`, `focus_actor_pitch_deg`, `focus_actor_roll_deg` | 所聚焦主体的世界朝向（度）；当 `focus_hit=0` 时为空  |
| `gaze_velocity_deg_s`, `saccade_state`, `saccade_onset_s`, `saccade_amplitude_deg`, `saccade_peak_velocity_deg_s` | 角视线速度（度/秒）、实时 I-VT 扫视状态（注视`fixation`/扫视`saccade`）、起始模拟时间（秒）、幅度（度）以及峰值速度（度/秒） |
| `sample_dt_ms` | 与上一条记录行相比的仿真时间增量（毫秒） |

#### 可选的手部姿态列（18 列，对应 `-HandPose` 参数 / **记录控制器姿态**）

该部分插入在 `sample_dt_ms` 之前，仅当 `-DReyeVRHandPose` 参数传入引擎时（启动器参数：`-HandPose`；图形界面选项：**记录手柄位姿**）才会填充数据。若未启用该选项，这 18 列依然存在但保持为空，因此在读取数据时，总列数始终不变，但其中*已填充*数据的列数会发生变化。

| 列 | 描述 |
| --- | --- |
| `hand_l_valid`, `hand_r_valid` | 若运行时在本帧为该控制器报告了有效的追踪姿态则为`1`；否则为 `0`。 |
| `hand_l_x_m`, `hand_l_y_m`, `hand_l_z_m`, `hand_r_x_m`, `hand_r_y_m`, `hand_r_z_m` | 控制器（握柄）框架原点，**OpenVR 站立式追踪空间，米**  |
| `hand_l_pitch_deg`, `hand_l_yaw_deg`, `hand_l_roll_deg`, `hand_r_pitch_deg`, `hand_r_yaw_deg`, `hand_r_roll_deg` | 直接从右手系 OpenVR 列基矩阵分解出的控制器朝向，以固有 `Y(yaw)-X(pitch)-Z(roll)` 欧拉角（单位：度）表示。  |
| `hand_l_trigger`, `hand_r_trigger` | 来自旧版 OpenVR 的扳机轴（`rAxis[0]`），标称范围为 `0..1`。 |
| `hand_l_grip`, `hand_r_grip` | 来自 `rAxis[1]` 的握持/挤压轴，标称范围为 `0..1` |

诚实说明（局限性），请在分析前阅读：

- 文中的位姿数据基于 **OpenVR 的“站立追踪空间”（单位：米）**，而非 UE 或 CARLA 的世界坐标系。若无明确的坐标变换，这些数据无法直接与 `head_*_m`、`vehicle_*_m` 或任何 `focus_*_m` 列中的数据进行比较；即便执行相同的动作，若在 SteamVR 中重新设定了中心点（或处于不同的游玩空间），所记录的位姿数值也会有所不同。 
- 扳机键（`trigger`）和握柄键（`grip`）的数据源自传统的 OpenVR 轴数组（`rAxis[0]`、`rAxis[1]`）。在 SteamVR 环境下的 Pimax Dream Air 设备上，这些轴当前返回的值为 `0.000`；而未分配的轴（值 < `-0.5`）则会被标记为空。因此，在将 `0.000` 视为“未按下”状态之前，请务必先确认该轴的数值是否确实发生了变化。
- **未记录手指关节信息**。控制器仅提供刚体 6 自由度（6-DoF）位姿以及两个标量轴数据；不包含各手指的弯曲状态。手指姿态需根据推断得出（请参阅下方的回放说明）。
- 当 `hand_*_valid=0`、相关选项处于关闭状态，或处于 VR 环境之外时，这些列将保持为空。 

### 2. 高频注视数据流 `<session>_gaze.csv`（18 列）

在眼动仪的原生采样网格上记录，并包含扫视（saccade）判定结果（含闭合事件）：

| 列 | 描述 |
| --- | --- |
| `device_time_ms`, `host_recv_s`, `sim_time_s`, `ue_frame` | 追踪器时间戳（毫秒）、主机接收时间（秒）、仿真时间（秒）以及 UE 帧编号  |
| `comb_h_deg`, `comb_v_deg`, `l_h_deg`, `l_v_deg`, `r_h_deg`, `r_v_deg` | 由运行时系统（Pimax PVR 1.33.1）报告的综合“独眼”（cyclopean）视角（水平/垂直，单位：度）以及各单眼的原始视野数据（其中 `l_*` 和 `r_*` 是基于融合后的“独眼”射线合成的，并带有 `4.0000 度`的固定水平偏移；分析时请使用 `comb_h_deg` 和 `comb_v_deg`） |
| `vergence_deg`, `valid` | 两条运行时射线之间的夹角（度；在 Pimax PVR 上合成，请勿用于辐辏分析）以及采样有效性（`1`/`0`）  |
| `gaze_vel_deg_s`, `saccade_state` | 瞬时注视角速度（度/秒）及事件判定结果（注视`fixation`、扫视`saccade`、已剔除`rejected`，或扫视_未闭合`saccade_open`） |
| `saccade_onset_s`, `saccade_amp_deg`, `saccade_peak_deg_s`, `saccade_samples` | 闭合扫视事件的起始时间（秒）、幅度（度）、峰值速度（度/秒）以及采样点数（同一闭合事件的所有行中该数值均相同） |

坐标采用 UE/CARLA 左手坐标系（X 轴向前，Y 轴向右，Z 轴向上），并支持大地图原点偏移。唯一的例外是可选的 `hand_*` 数据块，其采用的是 OpenVR 原始追踪空间（单位：米）。当 `gaze_valid=0` 时，车辆（vehicle）和道路（road）相关列仍会写入数据，而视线（gaze）和焦点（focus）坐标则保持为空。


## 肌肉骨骼运动回放

已录制的“手部”`hand_*`数据块可用于驱动离线状态下的上肢数字人：`Util/HandPose/record_hands.py` 可直接捕获控制器与头显（HMD）的位姿（无需模拟器）；`Util/HandPose/replay_arms.py` 则通过 MuJoCo 的 MS-Human-700 模型回放 CSV 数据。该过程集成了基于解剖学的逆运动学（IK）、方向盘几何结构与旋转（`steer_input`）、控制器外壳边缘的偏移补偿，以及基于逆动力学的肌肉激活状态可视化（通过颜色呈现），并最终输出 MP4 视频文件及起始、中间、结束时刻的静态截图。实时 VR 虚拟角色（`ADReyeVRPawn`）与 `replay_arms.py` 均采用同一套“一次性自动校准”机制（`FDReyeVRAutoCalibrator`）：当头部保持静止（`5 秒内`位移 `< 5 厘米`且旋转 `< 6 度`），随后方向盘转动幅度达到一定阈值（`>= 0.015`，即在 `900 度`转向盘上转动`约 6.8 度`）时，系统即完成校准。因此，驾驶员无需手动执行 VR 视点重置或手部校准操作。关于环境配置、具体指令（如 `--start`、`--fit`、`--raw-hands`、`--no-muscle`）以及系统局限性（包括手指预弯曲状态固定、腿部保持坐姿固定、肌肉激活状态由模型推断而非基于肌电信号（EMG）、控制器外壳偏移补偿与 `--raw-hands` 模式的区别，以及触及范围球体限制等），请参阅 [`Util/HandPose/README.md`](../Util/HandPose/README.md)。


## 筛选查询示例

- **转弯过程中的注视分配:** 筛选 `in_junction=1`、运动方向`motion`为左`left`/右`right`且 `gaze_valid=1` 的数据，随后对比 `steer_input`、`gaze_local_*`、`head_yaw_deg` 以及 `focus_*` 等指标。 
- **红灯处的制动行为:** 筛选出 `red_light_stop_candidate=1` 的数据，并按 `traffic_light_id` 进行分组，考察 `throttle_input`、`brake_input` 以及 `focus_*` 随 `sim_time_s` 的变化情况。


## 性能与验证

- `<session>.csv` 默认采用 **120 Hz** 的目标采样频率（每个渲染帧最多采样一次；对于低帧率场景，不进行人为插值；采样频率最低可配置为 **20 Hz**）。当启用 `-EyeThreadHz 120` 参数时，`<session>_gaze.csv` 会通过一个独立的 120 Hz 后台线程轮询眼动追踪设备，并运行经过校准的 I-VT 检测算法（起始阈值 120°/s，结束阈值 60°/s，最短持续时间 20 ms）。当仿真处于暂停状态时，不会写入任何采样数据。 
- CSV 写入程序采用缓冲 I/O 机制，数据会每秒刷新一次，并在会话结束时进行最终刷新。若磁盘写入失败，记录过程将停止，并记录日志：`Driving study: write failed`。 

开发者测试命令（在代码仓库根目录下运行）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Util\Tests\RunPimaxTests.ps1 -UE4Root '<UE4 source engine root>'
powershell -NoProfile -ExecutionPolicy Bypass -File .\Util\Tests\TestPimaxLauncher.ps1
powershell -NoProfile -STA -ExecutionPolicy Bypass -File .\StartDrivingStudy.ps1 -ValidateOnly
```
