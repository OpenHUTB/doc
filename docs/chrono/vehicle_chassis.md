# 车辆底盘
任何车辆系统都必须包含底盘子系统。车辆的位置、方向、速度和加速度均定义为底盘参考系。所有其他车辆子系统均相对于车辆底盘进行初始化。

目前仅提供一个底盘模板：[ChRigidChassis](https://api.projectchrono.org/classchrono_1_1vehicle_1_1_ch_rigid_chassis.html) ，由单个刚体组成。

为了对具有不同拓扑结构（例如铰接式底盘）、具有扭转柔顺性的底盘以及拖车系统进行建模，Chrono::Vehicle 还包括所谓的“后底盘”（基类 [ChChassisRear](https://api.projectchrono.org/classchrono_1_1vehicle_1_1_ch_chassis_rear.html) ，刚体模板 [ChRigidChassisRear](https://api.projectchrono.org/classchrono_1_1vehicle_1_1_ch_rigid_chassis_rear.html) ），它可以使用专门的“底盘连接器”连接到前底盘。

有以下三种类型的底盘连接器模板可供选择：

- [ChChassisConnectorArticulated](https://api.projectchrono.org/classchrono_1_1vehicle_1_1_ch_chassis_connector_articulated.html) 允许将前后底盘与驱动旋转关节连接起来，该旋转关节由转向驱动器输入控制。
- [ChChassisConnectorTorsion](https://api.projectchrono.org/classchrono_1_1vehicle_1_1_ch_chassis_connector_torsion.html) 允许使用具有指定扭转刚度的纵向旋转关节连接前后底盘。
- [ChChassisConnectorHitch](https://api.projectchrono.org/classchrono_1_1vehicle_1_1_ch_chassis_connector_hitch.html) 模拟拖车挂钩连接（使用球形接头）。