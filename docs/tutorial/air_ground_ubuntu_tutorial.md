# 空地一体协同智能载具虚拟仿真实验教程（Ubuntu / OpenHUTB）

> 本教程在 **Ubuntu** 上带你在 **OpenHUTB/hutb 官方包** 中跑通“地面车辆 + 无人机”的空地一体实验：先看到车机同框，再按六个模块完成场景构建、感知决策、无人机、空地协同、交通场景和 AI 辅助开发。
>
> **路径说明（务必先看）**：模拟器安装入口始终使用 OpenHUTB 主页的 `https://openhutb.github.io/dl.sh`，本文没有改成其他下载源。教程里有两套脚本根目录，不能混用：
> - `hutb/PythonAPI/...`：`dl.sh` 下载的模拟器包，空地一体脚本和 8 个分步教程在 `PythonAPI/examples/air/`。
> - `doc/src/...`：`OpenHUTB/doc` 文档仓库，感知、规划、交通类示例脚本在这里，**不在** `hutb/PythonAPI/examples/`。
>
> air_doc 上 Carla-Air 0.1.7 预编译包使用 `CarlaAir.sh` 和 `examples/`，目录布局与本教程的 hutb 包不同；本教程仍按 OpenHUTB 主页的 hutb 包编写。

## 实验基本信息

| 项目 | 内容 |
| --- | --- |
| 实验名称 | 空地一体协同智能载具虚拟仿真实验 |
| 操作系统 | Ubuntu 18.04 / 20.04 / 22.04（64 位） |
| 面向专业 | 人工智能、机器人工程、低空经济 |
| 实验课时 | 课程 32 学时，实验 16 学时 |
| 实验模块 | 6 个模块、29 个交互步骤 |
| 知识点 | 8 个 |
| 仿真底座 | OpenHUTB/hutb（已集成 Carla + AirSim 空地一体与无人机插件） |
| 开源许可 | MIT |

## 学习目标

完成本实验后，你将能够：

- 理解 OpenHUTB/hutb 中 Carla 与 AirSim 单进程空地一体仿真的基本架构，说清两者如何共享同一世界、同一套物理与传感器时间戳。
- 独立启动仿真环境，完成路网生成、场景保存、车辆与无人机连接。
- 配置相机、激光雷达、毫米波雷达等传感器，完成目标检测、点云可视化与多传感器数据采集。
- 编写 Python 脚本控制车辆与无人机，完成路径跟踪、航点飞行、多机编队与空地协同任务。
- 基于路口流量、车均延误、饱和度、排队长度、覆盖率、冲突次数等指标评价方案，并完成一次复测迭代。
- 按开源协作规范提交代码与文档，使用 GitHub Copilot 辅助读文档、改脚本、排查报错。

## 先修知识

- Python 基础：变量、循环、函数、常用库（numpy、matplotlib 均可）。
- Linux 基础：终端、路径、环境变量、`pip`/`venv`。
- ROS2 基础：节点、话题、服务的基本概念；没学过可先看平台前置微课。
- 控制与机器学习基础：PID、状态估计、目标检测的基本概念。

## 你将完成

- 启动 OpenHUTB/hutb，看到车辆与无人机在**同一个世界**中运行。
- 跑通 4 分屏传感器画面：RGB、深度图、语义分割、LiDAR 鸟瞰。
- 观察无人机跟踪地面车辆、天气切换、车机时间戳对齐。
- 按六个模块完成 29 个交互步骤，并提交实验报告与指标表。

## 开始前

### 硬件

- Ubuntu 18.04 / 20.04 / 22.04，64 位。
- 推荐 NVIDIA RTX 2070 及以上、显存 8 GB 及以上。
- 内存 16 GB 及以上；磁盘至少预留 50 GB。
- 已安装 NVIDIA 驱动，终端执行 `nvidia-smi` 能看到显卡信息。
- 只有核显或 8 GB 内存的机器可以看文档、写脚本，但跑模拟器会非常卡。

### 软件

- Git、Python 3.7+、pip、VS Code。
- **不需要单独下载额外发行包**：下面的 `dl.sh` 会下载 OpenHUTB/hutb 官方包，其中已集成空地一体与无人机插件。
- 浏览器（用于看文档和 GitHub）。
- 能访问 GitHub；如果无法访问，请使用可用的网络环境。

### 系统依赖

```bash
sudo apt update
sudo apt install -y git wget curl tar unzip build-essential python3-pip
```

### Ubuntu 环境检查

在开始前，先确认以下命令都能正常输出：

```bash
nvidia-smi
python3 --version
python3 -m pip --version
git --version
```

- `nvidia-smi` 没有输出：先装 NVIDIA 驱动并重启。
- `pip3` 找不到：先装 `python3-pip`，或改用 `python3 -m pip`。
- `python3` 版本低于 3.7：先升级 Python。

> **第一次学习不要从数字孪生开始。** 数字孪生需要编译 HUTB，最重、最容易卡；先跑模块二—五，最后再做模块一和数字孪生。

### 脚本目录约定

下面命令里的脚本分布在不同的目录，**每条命令先 `cd` 到对应目录**，不要假设当前目录：

| 脚本 | 正确位置 |
| --- | --- |
| 空地一体展示脚本（quick_start_showcase、air_ground_sync、drone_car_chase、demo_drive_and_fly） | `hutb/PythonAPI/examples/air/` |
| 8 个分步教程（01_hello_world 等） | `hutb/PythonAPI/examples/air/` |
| hutb 自带示例（generate_traffic、manual_control 等） | `hutb/PythonAPI/examples/` |
| 相机、边界框、点云、路径点脚本（rgb_camera_example、sensor_bounding_box、3d_lidar、waypoint_follow） | `doc/src/examples/`（OpenHUTB/doc 仓库） |
| 检测、轨迹、选点、规划、导航、交通指标脚本（object_detection、Drive、locate_moving、main_v4_VO、automatic_control_revised、traffic_indicators、signal_control、auto_signal_control、spectator） | `doc/src/course/...`（OpenHUTB/doc 仓库） |
| AirSim 多机示例（multi_agent_drone、add_drone、hello_drone） | `air` 仓库的 `PythonClient/multirotor/` |

`hutb/PythonAPI/examples/` 里**没有** `rgb_camera_example.py`、`sensor_bounding_box.py`、`3d_lidar.py`、`waypoint_follow.py`、`traffic_indicators.py`、`spectator.py` 这些文件，不要在这里找。以你本地发行包/仓库的实际路径为准；找不到时先 `ls` 看目录。

## 快速开始：30 分钟看到“车机同框”

下面以 Ubuntu 上的 OpenHUTB/hutb 官方包为例。所有命令都在终端里执行；首次运行需要联网下载依赖。

### 1. 下载 OpenHUTB/hutb 官方包

```bash
curl -fsSL -o dl.sh https://openhutb.github.io/dl.sh && chmod +x dl.sh && ./dl.sh
```

> 如果这一步报 `BadZipFile`，先不要反复重试；这是下载到的包不完整/服务器没有预编译包，排查方法见文末“常见问题”。

脚本会下载模拟器包；解压后进入生成的目录（通常叫 `hutb`，以实际解压结果为准）：

```bash
cd hutb
```

### 2. 启动模拟器

```bash
chmod +x CarlaUE4.sh
./CarlaUE4.sh
```

第一次启动会加载地图，比较慢，属正常现象。

### 3. 安装 Python 接口

```bash
python3 -m pip install PythonAPI/carla/dist/hutb-*.whl
python3 -m pip install pygame numpy
```

如果提示找不到文件，先确认 `PythonAPI/carla/dist/` 下确实有 `hutb-*.whl`。

### 4. 运行车机展示（另开一个终端）

```bash
cd <你的 hutb 目录>
python3 PythonAPI/examples/air/quick_start_showcase.py
```

你应该看到：一辆车在城市中自动巡航，无人机从空中追踪；4 分屏同时显示 RGB、深度图、语义分割、LiDAR 鸟瞰；天气自动轮换。按 `N` 手动切天气，按 `Esc` 退出。

> 这个脚本本身**不支持 WASD 接管驾驶**（源码里只注册了 `N` 和 `ESC`）。要键盘驾驶，另开终端运行 `python3 PythonAPI/examples/air/drive_vehicle.py`，那个脚本才是 `WASD` 驾驶、`Space` 手刹、`R` 倒车。

### 5. 运行空地同步

```bash
python3 PythonAPI/examples/air/air_ground_sync.py
```

左右分屏中，地面车辆与空中无人机处于同一世界、同一场天气；按 `N` 切换天气，按 `Esc` 退出。

### 成功标志

- 车与无人机出现在同一画面。
- 4 路传感器画面同时刷新。
- 切换天气时，地面和空中同时变化。
- 没有端口占用、API 版本不匹配的报错。

## 六个实验模块

| 模块 | 内容 | 关键脚本 / 操作 | 对应步骤 |
| --- | --- | --- | --- |
| 模块一 | 环境与数字孪生底座 | 启动模拟器、OSM 生成路网、保存地图 | 1—3 |
| 模块二 | 自动驾驶感知—决策—控制 | 相机、边界框、点云、目标检测、路径跟踪 | 4—12 |
| 模块三 | 无人机与低空资产 | 双客户端连接、起飞、多机、倾斜摄影 | 13—17 |
| 模块四 | 空地协同 | 车机分屏、联合展示、无人机跟踪车 | 18—19 |
| 模块五 | 交通场景与多载具协同 | 交通流、路口指标、信号控制、多机巡检 | 20—25 |
| 模块六 | 协作与 AI 辅助开发 | Fork、分支、Copilot、Pull Request | 26—29 |

## 模块一：环境与数字孪生底座（建议最后做）

**目标**：把真实路网变成仿真场景，并保存为可重复载入的地图。

1. 启动模拟器服务端并连接客户端：

   ```bash
   cd <你的 hutb 目录>
   ./CarlaUE4.sh
   ```

   再用 `config.py` 加载地图（在 hutb 包根目录执行）：

   ```bash
   python3 PythonAPI/util/config.py -m Town01
   ```

2. 由 OpenStreetMap 生成路网：打开数字孪生工具（CarlaTools 内容中的 `UW_OnRoadMainWidget`），填入 OSM 网址或导入本地 `.osm`，框选区域后点击生成。2×2 km² 约需 10 分钟。

3. 加载生成场景并保存：

   ```bash
   # 在 hutb 包根目录
   python3 PythonAPI/util/config.py -x *.xodr
   ```

   如果按文档仓库的写法运行，则要先进入 `OpenHUTB/doc` 仓库根目录，再执行 `python3 src/util/config.py -x *.xodr`；`src/` 是 doc 仓库的目录，不在 hutb 包里。

   保存地图可能耗时 1 小时以上；保存后在编辑器中检查车道与路口。

> 这一步依赖 HUTB 编译。第一次做建议在教师演示后完成，不要自行硬编。

## 模块二：自动驾驶感知—决策—控制

**目标**：让车辆“看得见、判得准、走得稳”。

```bash
# 以下脚本在 OpenHUTB/doc 仓库的 src/ 下运行；不是 hutb/PythonAPI/examples/
cd <你的 doc 仓库>/src

# 4. 多路相机（先另开终端运行 examples/manual_control.py 生成 hero）
python3 examples/rgb_camera_example.py --host localhost --port 2000 --rolename hero

# 5. 三维边界框（同样需要 hero）
python3 examples/sensor_bounding_box.py --host localhost --port 2000 --rolename hero --view above --distance 100 --res 800x600 --fov 90

# 6. 激光雷达点云（需要 hero 与 Open3D）
python3 examples/3d_lidar.py --host localhost --port 2000 --rolename hero --keep_ego_vehicle

# 7. YOLOv3 目标检测（在脚本目录运行，weights/ 与 cfg/ 是相对路径）
cd course/object_detection
python3 object_detection.py
cd ../..

# 8. 路径点跟踪（先在 hutb 终端运行 python3 PythonAPI/util/config.py -m Town01；json 路径相对 doc/src）
python3 examples/waypoint_follow.py --host localhost --port 2000 --rolename hero --map Town01 --json_file examples/data/town01_waypoints.json --sync --fixed_delta_seconds=0.05 --spawn --visualize --camera_follow

# 9. 轨迹跟踪（湖工商场景；先运行 examples/generate_traffic.py）
python3 course/trajectory_tracking/Drive.py

# 10. 地图选点移动
python3 course/locate_moving.py

# 11. 路线规划（同级有 motion_primitve.py / basic_PID.py，必须在本目录运行）
cd course/Motion_Planning
python3 main_v4_VO.py
cd ../..

# 12. 校园轨迹（--s/--e 可取 北门、西门、楚枫桥、楚枫轩、日新楼、体育馆、湘江楼、科技楼）
python3 course/navigation/automatic_control_revised.py --s 北门 --e 西门 --speed 5
```

> 这些脚本依赖 `OpenHUTB/doc` 仓库的 `src/`，hutb 包里没有 `course/`。`rgb_camera_example.py`、`sensor_bounding_box.py`、`3d_lidar.py` 需要先在另一个终端运行 `manual_control.py` 生成 `hero` 车辆，否则会报 `Actor hero not found`。`object_detection.py` 还需要自行准备 `weights/yolov3.weights`（仓库只带 `cfg/`）。`Drive.py`、`automatic_control_revised.py`、`traffic_indicators.py`、`spectator.py` 依赖湖工商场景。

**成功标志**：相机画面同步、边界框与车辆对齐、点云能看出道路与车辆轮廓、检测框随视角变化、车辆能沿路点或规划路径行驶。

## 模块三：无人机与低空资产

**目标**：连接 Carla 与 AirSim 双客户端，完成起飞、多机添加和航拍建模。

1. 启动 OpenHUTB/hutb 模拟器，加载校园地图（如 `Town10HD`），分别连接 Carla 客户端（端口 `2000`）和 AirSim 多旋翼客户端（端口 `41451`）。

2. 基础飞行与分步教程：

   ```bash
   cd <你的 hutb 目录>
   python3 PythonAPI/examples/air/01_hello_world.py
   python3 PythonAPI/examples/air/05_drone_takeoff.py
   ```

3. 继续完成天气、交通流、无人机起飞等示例：

   ```bash
   python3 PythonAPI/examples/air/02_weather_control.py
   python3 PythonAPI/examples/air/03_spawn_traffic.py
   ```

   多机示例见 `air` 仓库的 `PythonClient/multirotor/`：`multi_agent_drone.py`、`add_drone.py`、`hello_drone.py` 都在这里，**不在** hutb 包的 `PythonAPI/examples/air/` 里。如果还没克隆 air 仓库，或当前包内没有这些脚本，先完成单车/单机示例。

4. 倾斜摄影与三维重建：用手机或相机固定焦距绕建筑拍摄约 60 张、相邻重叠度不低于 70% 的照片，按 Meshroom 教程完成 SfM、深度图、网格与纹理，导出 `.obj`；也可按 `air_3d` 文档用 ContextCapture 重建校园建筑。

**成功标志**：无人机能起飞/悬停/降落；多机能独立控制；重建模型能导入虚幻引擎。

## 模块四：空地协同

**目标**：让无人机和地面车辆在同一世界协同。

```bash
# 左右分屏：同一场雨、同一个世界
python3 PythonAPI/examples/air/air_ground_sync.py

# 四路传感器 + 无人机追踪车辆
python3 PythonAPI/examples/air/quick_start_showcase.py

# 无人机跟踪地面车辆
python3 PythonAPI/examples/air/drone_car_chase.py

# 一个脚本同时驱动车辆与无人机
python3 PythonAPI/examples/air/demo_drive_and_fly.py
```

**成功标志**：两侧位姿与传感器时间戳逐帧对齐（坐标对齐误差 `0.0000 m`）；无人机能稳定跟踪车辆并回传机载画面；切换天气两侧同步。

## 模块五：交通场景与多载具协同

**目标**：在交通场景中加入多架无人机，评价车—机耦合效果。

实验按 **20 项算法测试矩阵**组织：感知 5、定位与地图 3、规划与决策 3、控制 1、交通 3、无人机与协同 3、学习 2。下面的交通脚本同样在 `OpenHUTB/doc` 仓库的 `src/` 下执行，不在 `hutb/PythonAPI/examples/`。

```bash
cd <你的 doc 仓库>/src

# 生成车流与行人（hutb 包里也有同名脚本，但这里用 doc 仓库的版本）
python3 examples/generate_traffic.py -n 50 -w 20 --safe

# 统计路口指标（依赖湖工商场景；脚本内固化了两个路口坐标）
python3 course/traffic_indicators.py

# 手动信号控制：先启动 Flask 服务，再发请求
python3 course/signal_control.py
# 浏览器或 curl 请求：
# http://127.0.0.1:5000/set_traffic_light?traffic_id=-5&color_id=3&color_time=30

# 自动感应控制（做对比实验时用）
python3 course/auto_signal_control.py
# http://127.0.0.1:5000/set_traffic_light

# 四个预设路口视角轮换（不是多机分区巡检）
python3 course/spectator/spectator.py
```

`traffic_indicators.py` 和 `spectator.py` 都需要湖工商场景，且 `traffic_indicators.py` 的路口范围写死在脚本里（桐梓坡路—西二环、桐梓坡路—望岳）；没有该场景时，脚本可能能连上模拟器但指标没有意义。

再做两组对比：

- 改变车辆数（20、50、100 辆），记录排队长度、车均延误、饱和度。
- 改变无人机数量（1、2、3 架），记录覆盖率、任务完成时间、空地冲突次数。

**成功标志**：改配时后指标实时变化；多机增加时覆盖率上升，冲突次数随分配规则变化，能找到饱和度/协同负载的拐点。

## 模块六：协作与 AI 辅助开发

**目标**：按开源协作流程提交成果，并用大模型辅助开发。

1. Fork 并克隆仓库，新建分支（把 `你的用户名`、`仓库名` 换成实际值，例如 `hutb` 或 `doc`）：

   ```bash
   git clone https://github.com/你的用户名/仓库名.git
   cd 仓库名
   git switch -c docs-fix-contribution-steps
   git status
   git diff
   ```

2. 按 GitHub Copilot 文档启用 Copilot，在 VS Code 中登录，让它解释一段 OpenHUTB 文档中的调用链。

3. 让模型补全或改写 `examples` 中的示例脚本（如增加传感器、改变车速），在模拟器中运行验证，逐行核对改动。

4. 提交：

   ```bash
   git add 你实际修改的文件
   git diff --cached
   git commit -m "docs: 说明本次修改"
   git push -u origin docs-fix-contribution-steps
   ```

   把 `你实际修改的文件` 换成实际文件名（如 `CONTRIBUTING.md`），不要照抄占位符。贡献指南要求 `git add` 具体文件，而不是 `git add .`；提交前用 `git diff --cached` 再核对一次。创建目标为 OpenHUTB 的 Pull Request，按评审意见修改后合并，并提交实验报告与指标对比表。

## 实验报告要求

实验报告建议包含以下内容：

1. **实验环境**：操作系统、显卡、Python 版本、OpenHUTB/hutb 版本。
2. **过程记录**：每个模块的关键命令、运行截图、遇到的问题与解决办法。
3. **指标表**：路口流量、车均延误、饱和度、排队长度；多机实验的覆盖率、任务完成时间、冲突次数。
4. **结果分析**：不同参数下指标如何变化，是否与预期一致；失败情形的原因与改进。
5. **成果链接**：代码分支、Pull Request、实验数据或录屏（如有）。

报告以“能复现、能解释、有证据”为标准，不接受只有截图、没有指标与分析的报告。

## 结果与评价

完成实验后，你应该能复现以下结果：

- 数字孪生：路网可保存、可重复载入；2×2 km² 生成约 10 分钟，保存约 1 小时。
- 感知：雨雾/夜间下检测框数量和置信度下降；点云远处变稀疏。
- 控制：步长越小、采样越密，轨迹误差越小。
- 无人机：多机分层飞行时，覆盖率、冲突次数可比较；中等联合配置约 `19.8±1.1 FPS`。
- 空地协同：车机时间戳逐帧对齐，坐标误差 `0.0000 m`。
- 交通场景：流量上升时排队、延误、饱和度上升，可找临界流量。

成绩构成：

| 维度 | 权重 | 看什么 |
| --- | --- | --- |
| 参与度 | 40% | 前测/出勤、角色承担、Commits、Issues 讨论、PR 数量与审核评论 |
| 提交规范性 | 20% | 分支命名、提交信息、PR 描述、代码风格、文档格式 |
| 作业质量 | 40% | 步骤完成度、指标表与复算、实验报告、创新与复测 |

等级：不及格、及格、中、良、优。

## 常见问题

**Q：只有核显/8 GB 内存能跑吗？**
可以看文档、写脚本，跑模拟器会非常卡。建议用带 NVIDIA 独显、16 GB 内存以上的机器做模块三—五。

**Q：运行 `./dl.sh` 报 `BadZipFile`？**

`dl.sh` 只是下载器，真正的模拟器包由它从服务器拉取。报 `BadZipFile` 通常不是 Ubuntu 的问题，而是下载到的文件不是完整 zip：服务器返回了 404/HTML 页面、下载中断，或网络加速器改写了内容。

按下面顺序排查：

1. 重新执行一次 `./dl.sh`，不要连续重试十几次。
2. 找到刚下载的 zip，检查它是不是真的 zip：

   ```bash
   find ~ -name '*.zip' -mmin -30 -ls
   file 下载到的.zip
   unzip -t 下载到的.zip
   ```

   - `file` 显示 HTML/ASCII：下载到的是网页，不是包。
   - `unzip -t` 报错：包不完整，重新下载或换网络。

3. 如果服务器上**只有源码、没有预编译包**，`dl.sh` 解决不了：向老师/学长要 **Ubuntu 预编译包**（整个 `hutb` 目录），或申请实验室机器；不要在 8 GB 核显笔记本上从源码编译 UE4.26。
4. 如果老师给了压缩包，解压后直接运行 `CarlaUE4.sh`，不需要再跑 `dl.sh`。

**Q：运行 `./CarlaUE4.sh` 提示 Permission denied？**
先赋予执行权限：`chmod +x CarlaUE4.sh`，再运行。

**Q：`nvidia-smi` 找不到命令？**
说明 NVIDIA 驱动没装好；先装驱动、重启，再确认 `nvidia-smi` 能输出显卡信息。

**Q：`pip install hutb-*.whl` 找不到文件？**
先确认你在 `hutb/PythonAPI/carla/dist/` 下能看到 `hutb-*.whl`；没有就重新运行 `./dl.sh` 或检查下载是否完整。

**Q：端口被占用？**
Carla 用 `2000`，AirSim 用 `41451`；先关掉旧进程，再重启。

**Q：数字孪生为什么最后做？**
它需要编译 HUTB，依赖 UE4.26、Ubuntu 编译工具链和较大的磁盘/内存；先把轻量模块跑通，再碰它。

**Q：GitHub 打不开？**
先检查网络与代理设置；如果仍然失败，换一个网络环境再试，并把完整报错记录下来。

## 参考

- 模拟器下载入口（保持不变）：https://openhutb.github.io/dl.sh
- OpenHUTB/hutb：https://github.com/OpenHUTB/hutb
- OpenHUTB/doc 文档仓库：https://github.com/OpenHUTB/doc
- 文档站：https://openhutb.github.io/doc/
- 空域文档：https://openhutb.github.io/air_doc/
- 交通教程参考：https://openhutb.github.io/doc/tutorials/
- 空地一体（Carla-Air 0.1.7）：https://openhutb.github.io/air_doc/dev/Carla_Air/
- AirSim Ubuntu 构建（air_doc）：https://openhutb.github.io/air_doc/build_linux/
- HUTB/Carla Ubuntu 构建（doc）：https://openhutb.github.io/doc/build_linux/
- 多车辆：https://openhutb.github.io/air_doc/multi_vehicle/
- 图像 API：https://openhutb.github.io/air_doc/image_apis/
- 贡献指南（渲染页）：https://openhutb.github.io/.github/CONTRIBUTING/
- 贡献指南（源文件）：https://github.com/OpenHUTB/.github/blob/master/CONTRIBUTING.md
