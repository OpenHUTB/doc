# [ROS 桥](https://carla.readthedocs.io/projects/ros-bridge/en/latest/)

---

ROS 桥可实现 ROS 和 Carla 之间的双向通信。来自 Carla 服务器的信息被转换为 ROS 主题。以同样的方式，ROS 中的节点之间发送的消息被转换为要在 Carla 中应用的命令。

ROS 桥与 ROS 1 和 ROS 2 兼容。

ROS 桥具有以下特点：

- 为激光雷达、语义激光雷达、相机（深度、分割、rgb、dvs）、全球导航卫星系统、雷达和惯性测量单元提供传感器数据。
- 提供对象数据，例如变换、交通信号灯状态、可视化标记、碰撞和压线。
- 通过转向、油门和制动控制自动驾驶代理。
- 控制 Carla 模拟的各个方面，例如同步模式、播放和暂停模拟以及设置模拟参数。

## 开始使用

- [__通过虚拟机设置并连接到 Carla 仿真器__](https://openhutb.github.io/ros2/set_up_and_connect_to_carla/)
- [__为 ROS 1 安装 ROS 桥__](ros_installation_ros1.md)
- [__为 ROS 2 安装 ROS 桥__](ros_installation_ros2.md)
- [__向 Carla 添加新的 ROS 2 消息类型__](./ros2/adding_message_types.md)


---

## 了解主要的 ROS 桥接包

- [__Carla 的 ROS 桥__](run_ros.md) - 运行 ROS 桥所需的主包
- [__ROS 兼容性节点__](ros_compatibility.md) - 允许相同 API 调用 ROS 1 或 ROS 2 函数的接口

---

## 了解额外的 ROS 桥接包

- [__Carla 生成对象__](carla_spawn_objects.md) - 提供生成参与者的通用方法
- [__Carla 手动控制__](carla_manual_control.md)- 用于自主车辆的基于 ROS 的可视化和控制工具（类似于 Carla 提供的`carla_manual_control.py`）
- [__Carla 阿克曼控制__](carla_ackermann_control.md) - 一个将阿克曼命令转为转向/油门/刹车的控制器
- [__Carla 路径点发布器__](carla_waypoint.md) - 发布和查询 Carla 路径点
- [__Carla 自动驾驶代理__](carla_ad_agent.md) - 遵循路线、避免碰撞并遵守交通信号灯的示例代理
- [__Carla 自动驾驶示例__](carla_ad_demo.md) - 一个示例包，提供使用自动驾驶车辆启动 Carla ROS 环境所需的一切
- [__Carla ROS Scenario Runner__](carla_ros_scenario_runner.md) - 通过 ROS 使用 Carla Scenario Runner 执行 OpenScenarios 的包装器
- [__Carla 扭转控制__](carla_twist_to_control.md) - 将扭转控制转换为 Carla 车辆控制
- [__RVIZ 插件__](rviz_plugin.md) - 用于可视化/控制 Carla 的 RVIZ 插件
- [__RQT 插件__](rqt_plugin.md) - 用于控制 Carla 的 RQT 插件
- [__PCL 记录器__](pcl_recorder.md) - 根据模拟捕获的数据创建点云地图

---

## 探索参考资料

- [__ROS 传感器__](ros_sensors.md) - 不同传感器中可用的参考主题
- [__ROS 消息__](ros_msgs.md) - Carla ROS 消息中提供的参考参数

