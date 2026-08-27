**入门示例**

1. 下载 [链接](https://pan.baidu.com/s/1n2fJvWff4pbtMe97GOqtvQ?pwd=hutb) 中的 software/hutb/hutb_car_vr_air_mujoco.zip，解压运行 CarlaUE4.exe 启动场景，按 W、S、A、D 键进行场景浏览；

2. 安装特定 Python 版本的功能包：`pip install PythonAPI/carla/dist/hutb-*.whl`（或者使用`pip install hutb` 安装 ），然后运行 [PythonAPI/examples](https://github.com/OpenHUTB/hutb/tree/hutb/PythonAPI/examples) 中的脚本（如果运行报错，请参考 [解决方法](faq/use_faq.md)）：

     * 运行 `python manual_control.py  --filter walker.pedestrian.*` 生成键盘控制的人，运行 [manual_control.py](https://github.com/OpenHUTB/doc/blob/master/src/examples/manual_control.py) 生成一辆键盘控制的车
     * 运行 [generate_traffic.py](https://github.com/OpenHUTB/doc/blob/master/src/examples/generate_traffic.py) 生成人车流
     * [切换](ue/switch_mode.md) 到 [VR 模式](interbehavior.md) ：[config.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/util/config.py) --map Town10HD?GAME=VR ；切换到 [无人机模式](https://openhutb.github.io/air_doc/) ：`config.py --map Town10HD?GAME=AIR`

### 基础 <span id="primary"></span>

[__介绍__](start_introduction.md) — 对 OpenHUTB 的期望

[__快速启动__](start_quickstart.md) — 获取 OpenHUTB 版本

[__第一步__](tuto_first_steps.md) — 开始进行 OpenHUTB 操作，介绍最重要的概念

[__示例__](tuto_E_gallery.md) — OpenHUTB 经典示例

[__教程__](tutorials.md) — OpenHUTB 详细教程


<!-- ## 主题 -->

[__基础__](foundations.md) — OpenHUTB 服务器和客户端进行操作和通信所需的基本概念

[__第一、 世界和客户端__](core_world.md) — 管理和访问模拟

[__第二、 参与者和蓝图__](core_actors.md) — 了解参与者以及如何处理它们

[__第三、地图和导航__](core_map.md) — 发现不同的地图以及车辆如何移动

[__第四、传感器和数据__](core_sensors.md) — 使用传感器检索模拟数据

[__检索模拟数据__](tuto_G_retrieve_data.md) — 使用记录器正确收集数据的分步指南

[__边界框__](tuto_G_bounding_boxes.md) — 将 OpenHUTB 对象的边界框投影到相机中

[__快速入门附加项__](./ext_quickstart.md) — 包含安装和运行 OpenHUTB 模拟器软件包版本的更多选项和详细信息

[__扩展文档__](./ext_docs.md) — 有关 OpenHUTB 许多广泛功能的深入文档

[__使用常见问题__](faq/use_faq.md) — 解决最常见的使用问题