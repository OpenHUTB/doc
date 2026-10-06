
# 定位
## 定位模块介绍

ISS 定位模块确保自动驾驶车辆不仅了解其在广阔的道路和环境中的位置，而且具有无与伦比的准确性。在本文档中，我们概述了当前的流程，从单个传感器到传感器融合算法。

## 单独的传感器

为了实现精确定位，采用了多方面的方法，使用各种传感器和算法：

1. **激光雷达**：
   - **迭代最近点(Iterative Closest Point, ICP)**<a href="#ref1"><sup>[1]</sup></a>：该算法对齐两个点云以确定对齐它们的最佳拟合变换。
   - **正态分布变换(Normal Distributions Transform, NDT)**<a href="#ref2"><sup>[2]</sup></a>: 这种先进的方法使用正态分布表示点云数据，提供了一种强大而有效的配准方法。

2. **惯性测量单元(Inertial Measurement Unit, IMU)**:
   - **航位推算**：通过利用运动传感器数据，航位推算可以连续估计车辆的位置。然而，随着时间的推移，其准确性会降低，需要补充数据进行修正。

3. **全球定位系统(Global Positioning System, GPS)**:
   - 虽然 GPS 为定位提供了全球参考，但其精度可能不足以满足自动驾驶的严格公差要求。因此，GPS 数据通常与其他传感器数据融合以提高准确性。

## 传感器融合

精准定位的关键不仅在于传感器的个体能力，还在于它们的协作能力：

1. **基于滤波器的方法**:
   - 递归算法，例如 **卡尔曼滤波器** 和 **粒子滤波器**<a href="#ref3"><sup>[3]</sup></a>，对于实时状态估计和预测是必不可少的。

2. **基于优化的方法**:
   - **GraphSLAM**<a href="#ref4"><sup>[4]</sup></a> 等整体方法可以调整和细化整个轨迹或地图，确保后处理场景中的最高准确性。

## 实施路线图
1. 维护激光雷达（迭代最近点、正太分布变换）、惯性测量单位（航位推测）、全球定位系统和基于滤波器的融合。
2. 研究基于优化的融合：GraphSLAM、绑定调整、位姿图优化。
3. 收集和处理优化方法的数据集。
4. 将基于优化的融合集成到当前的管道中。

## 参考文献
<ol>
    <li id="ref1">Besl P J, McKay N D. Method for registration of 3-D shapes. In <i>Sensor fusion IV: control paradigms and data structures</i>. Spie, 1992, 1611: 586-606.</li>
    <li id="ref2">Biber P, Straßer W. The normal distributions transform: A new approach to laser scan matching. In <i>Proceedings 2003 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2003)</i>. IEEE, 2003, 3: 2743-2748.</li>
    <li id="ref3">Thrun S. Probabilistic robotics. In <i>Communications of the ACM</i>, 2002, 45(3): 52-57.</li>
    <li id="ref4">Shan T, Englot B, Meyers D, et al. Lio-sam: Tightly-coupled LiDAR inertial odometry via smoothing and mapping. In <i>2020 IEEE/RSJ international conference on intelligent robots and systems (IROS)</i>. IEEE, 2020: 5135-5142.</li>
</ol>

