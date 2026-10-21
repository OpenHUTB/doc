# ROS2 原生示例

此示例演示了如何在 CARLA 中使用 ROS 2 原生接口。


## 先决条件

要运行此示例，请确保系统已安装 Docker。Docker 用于启动 RViz，可视化传感器数据。


## 使用

### 第 1 步：在启用 ROS2 的情况下启动 CARLA 模拟器

在启用 ROS 2 集成的情况下启动 CARLA 模拟器：

```bash
# 如果运行二进制包：
./CarlaUE4.sh --ros2

# 如果运行编辑器：
make launch ARGS="--ros2 --editor-flags='--ros2'"
```

### 第 2 步：运行 ROS2 示例

执行 ROS 2 示例脚本：

```bash
python3 ros2_native.py --file stack.json
```

* `stack.json` 文件定义传感器配置。
* 您可以编辑此文件以根据您的要求调整传感器设置。


### 第 3 步：运行 RViz 以可视化传感器数据 

启动`rviz` 以可视化 CARLA 的传感器输出：

> [!NOTE]
必须在您的系统上安装 Docker 才能完成此步骤。

```bash
./run_rviz.sh
```
