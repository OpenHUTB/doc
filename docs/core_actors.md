# 第二、参与者和蓝图

OpenHUTB 中的参与者是在模拟中执行动作的元素，他们可以影响其他参与者。OpenHUTB 的参与者包括车辆和行人，也包括传感器、交通标志、交通信号灯和观看者。对如何操作它们有充分的了解是至关重要的。 

本节将介绍生成、销毁、类型以及如何管理它们。然而，可能性几乎是无穷无尽的。实验、查看本文档中的 __教程__，并在 [OpenHUTB 论坛](https://github.com/OpenHUTB/hutb/discussions) 中分享疑虑和想法。

- [__蓝图__](#blueprints)  
	- [管理蓝图库](#managing-the-blueprint-library)  
- [__参与者生命周期__](#actor-life-cycle)  
	- [生成](#spawning)  
	- [处理](#handling)  
	- [销毁](#destruction)  
- [__参与者类型__](#types-of-actors)  
	- [传感器](#sensors)  
	- [观察者](#spectator)  
	- [交通标志和交通信号灯](#traffic-signs-and-traffic-lights)  
	- [车辆](#vehicles)  
	- [行人](#walkers)  

---
## 蓝图 <span id="blueprints"></span>

这些布局允许用户将新的参与者平滑地结合到模拟中。它们已经是带有动画和一系列属性的模型。其中一些是可修改的，而另一些则不是。这些属性包括车辆颜色、激光雷达传感器中的通道数量、行人的速度等等。

[蓝图库](bp_library.md) 列出了可用的蓝图及其属性。车辆和行人蓝图具有一个生成属性，用于指示它们是新的（第 2 代）资产还是旧的（第 1 代）资产。

### 管理蓝图库 <span id="managing-the-blueprint-library"></span>

[carla.BlueprintLibrary](python_api.md#carla.BlueprintLibrary) 类包含一系列 [carla.ActorBlueprint](python_api.md#carla.ActorBlueprint) 元素。它是能够提供对它访问的世界对象。
```py
blueprint_library = world.get_blueprint_library()
```
蓝图有一个 ID 来识别它们和由此产生的参与者。可以读取库来找到某个 ID，随机选择蓝图，或者使用 [通配符模式](https://tldp.org/LDP/GNU-Linux-Tools-Summary/html/x11655.htm) 过滤结果。

```py
# 找一个指定的蓝图
collision_sensor_bp = blueprint_library.find('sensor.other.collision')
# 随机选择一个车辆蓝图
vehicle_bp = random.choice(blueprint_library.filter('vehicle.*.*'))
```

除此之外，每个 [carla.ActorBlueprint](python_api.md#carla.ActorBlueprint) 能获取 _get_ 和改变 _set_ 一些列参与者属性 [carla.ActorAttribute](python_api.md#carla.ActorAttribute) 。
```py
is_bike = [vehicle.get_attribute('number_of_wheels') == 2]
if is_bike:
    vehicle.set_attribute('color', '255,0,0')
```
!!! 笔记
    某些属性无法修改。在[蓝图库](bp_library.md)中查看。

属性有一个参与者属性类型 [carla.ActorAttributeType](python_api.md#carla.ActorAttributeType) 变量。它从枚举列表中声明其类型。此外，可修改的属性还附带一个 __推荐值列表__ 。

```py
for attr in blueprint:
    if attr.is_modifiable:
        blueprint.set_attribute(attr.id, random.choice(attr.recommended_values))
```
!!! 笔记
    用户可以创建他们自己的车辆。查看 __教程（资产）__ 以了解相关信息。贡献者可以 [将他们的新内容添加到 Carla](tuto_D_contribute_assets.md) 。

---
## 参与者生命周期   <span id="actor-life-cycle"></span>

!!! 重要
    本节提到了关于参与者的不同方法。Python API 提供 __[commands](python_api.md#command.SpawnActor)__ ，以便在一个框架中应用一批最常见的命令。 

### 生成 <span id="spawning"></span>

__世界对象负责生成参与者并跟踪这些参与者。__ 生成只需要一张蓝图和一个 [carla.Transform](python_api.md#carla.Transform) 说明参与者的位置和旋转。 

世界有两个不同的方法生成参与者。 

* [`spawn_actor()`](python_api.md#carla.World.spawn_actor) 如果生成失败抛出一个异常。
* [`try_spawn_actor()`](python_api.md#carla.World.try_spawn_actor) 如果生成失败返回 `None`。

```py
transform = Transform(Location(x=230, y=195, z=40), Rotation(yaw=180))
actor = world.spawn_actor(blueprint, transform)
```

!!! 重要
    Carla 使用 [虚幻引擎坐标系统](python_api.md#carlarotation) 。记住： [`carla.Rotation`](https://openhutb.github.io/doc/python_api/#carlarotation) 构造函数定义为“俯仰、偏航、横滚`(pitch, yaw, roll)`” ，与虚幻引擎的“横滚、俯仰、偏航`(roll, pitch, yaw)`” 不同。

如果在指定位置发生冲突，将不会生成参与者。无论这种情况发生在静态对象还是其他参与者身上。可以尝试避免这些不希望的生成碰撞。

* __对于车辆__。 `map.get_spawn_points()` 返回推荐生成点的列表。

```py
spawn_points = world.get_map().get_spawn_points()
```

* __对于行人__。 `world.get_random_location()`返回人行道上的随机点。同样的方法也用于为行人设置目标位置。  

```py
spawn_point = carla.Transform()
spawn_point.location = world.get_random_location_from_navigation()
```

一个参与者在生成时可以附加到另一个参与者上。参与者跟随他们所依附的父级。这对于传感器特别有用。该附件可以是刚性的（适合检索精确数据），也可以根据其父级的情况进行轻松移动。它由辅助类 [carla.AttachmentType](python_api.md#carla.AttachmentType) 定义。

下一个示例将相机刚性地连接到车辆上，因此它们的相对位置保持固定。

```py
camera = world.spawn_actor(camera_bp, relative_transform, attach_to=my_vehicle, carla.AttachmentType.Rigid)
```
!!! 重要
    当生成附加的参与者时，提供的变换必须相对于父级参与者。

一旦生成，世界对象就会将参与者添加到列表中。这可以很容易地搜索或迭代。 
```py
actor_list = world.get_actors()
# 根据 id 找参与者
actor = actor_list.find(id)
# 打印世界上所有限速标志的位置。
for speed_sign in actor_list.filter('traffic.speed_limit.*'):
    print(speed_sign.get_location())
```

### 处理 <span id="handling"></span>

[carla.Actor](python_api.md#carla.Actor) 主要由  _get()_ 和 _set()_ 方法组成，用于管理地图周围的参与者。

```py
print(actor.get_acceleration())
print(actor.get_velocity())

location = actor.get_location()
location.z += 10.0
actor.set_location(location)
```

可以禁用参与者的物理特性以将其冻结在适当的位置。

```py
actor.set_simulate_physics(False)
```
除此之外，参与者还有他们的蓝图提供的标签。这些对于语义分割传感器最有用。

!!! 警告
    大多数方法是异步向模拟器发送请求。模拟器每次更新时解析这些请求的时间有限。如果大量使用 <font color="#7fb800">set()</font> 方法，会淹没模拟器，造成明显的延迟。


### 销毁 <span id="destruction"></span>

当 Python 脚本完成时，不会销毁参与者。他们必须明确地销毁自己。

```py
destroyed_sucessfully = actor.destroy() # 如果成功返回 True 
```

!!! 重要
    销毁参与者会阻塞模拟器，直到该过程完成。

---


## 参与者类型  <span id="types-of-actors"></span>

### 传感器 <span id="sensors"></span>

传感器是产生数据流的参与者。他们有自己的部分，[第四部分. 传感器和数据](core_sensors.md)。现在，我们只看一下常见的传感器生成周期。

此示例生成一个相机传感器，将其连接到车辆，并告诉相机将生成的图像保存到磁盘。

```py
camera_bp = blueprint_library.find('sensor.camera.rgb')
camera = world.spawn_actor(camera_bp, relative_transform, attach_to=my_vehicle)
camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame))
```

* 传感器也有蓝图。设置属性至关重要。
* 大多数传感器将安装在车辆上以收集周围环境的信息。
* 传感器 __监听__ 数据。收到数据后，它们会调用用 __[Lambda 表达式](https://docs.python.org/3/reference/expressions.html#lambda)__ 描述的函数。 

### 观察者 <span id="spectator"></span>

由虚幻引擎放置以提供游戏内的视角。它可用于移动模拟器窗口的视角。以下示例将移动观众参与者，将视角指向所需的车辆。

```py
spectator = world.get_spectator()
transform = vehicle.get_transform()
spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50),
carla.Rotation(pitch=-90)))
```

### 交通标志和交通信号灯 <span id="traffic-signs-and-traffic-lights"></span>

到目前为止，Carla 中只有停靠点、让行、交通信号灯被视为参与者。其余的 OpenDRIVE 标志可通过 API 作为地标（[__carla.Landmark__](python_api.md#carla.Landmark)）进行访问，他们的信息可以使用这些实例访问，但他们在模拟中并不作为参与者存在，在接下来的 __[地图和导航](https://openhutb.github.io/doc/core_map/#landmarks)__ 部分中将更详细地解释地标。 


当模拟开始时，会使用 OpenDRIVE 文件中的信息自动生成停止、让行和交通信号灯。__这些都无法在蓝图库中找到__，因此无法生成。

!!! 笔记
    OpenDRIVE 文件中的 Carla 地图没有交通标志或灯，这些是由开发人员手动放置的。注意：交通信号灯可以不包含在 OpenDRIVE 文件中（即可以不通过RoadRunner建模交通信号灯），而是在虚幻编辑器中添加交通信号灯。交通信号灯是作为参与者被PythonAPI读取，在OpenDRIVE中的被当成地标而不是参与者。

[__交通标志__](python_api.md#carla.TrafficSign) 未在路线图本身中定义，如下页所述。相反，他们有一个 [carla.BoundingBox](python_api.md#carla.BoundingBox) 来影响其中的车辆。 
```py
# 获得影响车辆的交通信号灯
if vehicle_actor.is_at_traffic_light():
    traffic_light = vehicle_actor.get_traffic_light()
``` 
路口设有[__交通信号灯__](python_api.md#carla.TrafficLight)。与任何参与者一样，他们有自己独特的 ID，但对于岔路口也有一个组（`group`） ID 。

同一组中的交通信号灯遵循一个循环。第一个交通信号灯设置为绿色，而其余交通信号灯则保持红色。活动的信号灯会花费几秒钟时间变绿、变黄、变红，因此有一段时间所有灯都是红色的。然后，下一个交通信号灯开始循环，前一个交通信号灯与其余交通信号灯一起冻结。

可以使用 API 设置交通信号灯的状态。每个状态花费的秒数也是如此。可能的状态用 [carla.TrafficLightState](python_api.md#carla.TrafficLightState) 描述为一系列枚举值。
```py
# 交通信号灯从红变绿
if traffic_light.get_state() == carla.TrafficLightState.Red:
    traffic_light.set_state(carla.TrafficLightState.Green)
    traffic_light.set_set_green_time(4.0)
``` 

!!! 笔记
    只有当信号灯为红色时，车辆才会意识到交通信号灯。

### 车辆 <span id="vehicles"></span>

[__carla.Vehicle__](python_api.md#carla.Vehicle) 是一种特殊类型的参与者。它采用了模拟轮式车辆物理特性的特殊内部组件。这是通过应用四种不同的控件来实现的：

* __[carla.VehicleControl](python_api.md#carla.VehicleControl)__ 提供油门、转向、刹车等驾驶命令的输入。
```py
vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=-1.0))
```
* __[carla.VehiclePhysicsControl](python_api.md#carla.VehiclePhysicsControl)__ 定义车辆的物理属性并包含另外两个控制器：

    * [carla.GearPhysicsControl](python_api.md#carla.GearPhysicsControl) 控制档位。
    * [carla.WheelPhysicsControl](python_api.md#carla.WheelPhysicsControl) 提供对每个轮子的特定控制。

```py
vehicle.apply_physics_control(carla.VehiclePhysicsControl(max_rpm = 5000.0, center_of_mass = carla.Vector3D(0.0, 0.0, 0.0), torque_curve=[[0,400],[5000,400]]))
```

车辆有一个 [carla.BoundingBox](python_api.md#carla.BoundingBox) 封装它们。该边界框允许将物理原理应用于车辆并检测碰撞。

```py
box = vehicle.bounding_box
print(box.location)         # 相对车辆的位置
print(box.extent)           # XYZ half-box extents in meters.
```

通过启用 [扫轮碰撞参数][enable_sweep] 可以改善车轮的物理特性。默认的轮子物理系统对每个轮子使用从轴到地板的单射线投射，但是当启用扫轮碰撞时，将检查轮子的整个体积是否发生碰撞。它可以这样启用：

```py
physics_control = vehicle.get_physics_control()
physics_control.use_sweep_wheel_collision = True
vehicle.apply_physics_control(physics_control)
```

[enable_sweep]: https://carla.readthedocs.io/en/latest/python_api/#carla.VehiclePhysicsControl.use_sweep_wheel_collision


车辆还包括其独有的其他功能：

* __自动驾驶模式__ 会将车辆订阅到 [交通管理器](adv_traffic_manager.md) 以模拟真实的城市状况。该模块是硬编码的，不是基于机器学习的。

```py
vehicle.set_autopilot(True)
```

* __车灯__ 必须由用户打开和关闭。每辆车都有一组在[__carla.VehicleLightState__](python_api.md#carla.VehicleLightState) 中列出的灯。并非所有车辆都集成了车灯。截至撰写本文时，配备集成车灯的车辆如下：

    * __自行车：__ 所有自行车都有前后位置灯。
  
    * __摩托车：__ 雅马哈和哈雷戴维森型号。
  
    * __汽车：__ 奥迪 TT、雪佛兰 Impala、道奇警车、道奇 Charger、奥迪 e-tron、林肯 2017 年和 2020 年、野马、特斯拉 Model 3、特斯拉 Cybertruck、大众 T2 和梅赛德斯 C 级。

可以使用 [carla.Vehicle.get_light_state](python_api.md#carla.Vehicle.get_light_state) 和 [carla.Vehicle.set_light_state](#python_api.md#carla.Vehicle.set_light_state) 方法随时检索和更新车辆的灯光。它们使用二进制运算来自定义灯光设置。

```py
# 打开位置灯
current_lights = carla.VehicleLightState.NONE
current_lights |= carla.VehicleLightState.Position
vehicle.set_light_state(current_lights)
```

### 行人 <span id="walkers"></span>

[__carla.Walker__](python_api.md#carla.Walker) 的工作方式与车辆类似。对它们的控制由控制器提供。

* [__carla.WalkerControl__](python_api.md#carla.WalkerControl) 以一定的方向和速度移动行人。它还允许他们跳跃。
* [__carla.WalkerBoneControl__](python_api.md#carla.WalkerBoneControl) 提供对三维骨架的控制。[本教程](tuto_G_control_walker_skeletons.md) 解释了如何控制它。

行人可以由人工智能控制。他们没有自动驾驶模式。[__carla.WalkerAIController__](python_api.md#carla.WalkerAIController) 参与者在它所附加的参与者周围移动。

```py
walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
world.SpawnActor(walker_controller_bp, carla.Transform(), parent_walker)
```
!!! 笔记
    人工智能控制器是无形的，没有物理特性。它不会出现在现场。此外，位置 `(0,0,0)` 相对于其父级的位置不会导致碰撞。  


__每个人工智能控制器都需要初始化、目标和可选的速度__。停止控制器的工作方式相同。

```py
world.tick()  # 在异步模式下使用 world.wait_for_tick()
ai_controller.start()
ai_controller.go_to_location(world.get_random_location_from_navigation())
ai_controller.set_max_speed(1 + random.random())  # 在 1 米每秒 到 2 米每秒之间（默认是 1.4 米每秒）
...
ai_controller.stop()
```

!!! 重要
    在生成“行人”（walker）与调用 `start()` 之间，世界必须至少经历一次“节拍”（tick）更新。`start()` 会从客户端接收到的最新快照中读取行人的位置，而在此快照之后生成的行人尚未包含在其中。若不经过这次“节拍”更新，行人将无法移动。

当行人到达目标位置时，他们会自动步行到另一个随机点。如果无法到达目标点，行人将前往距离当前位置最近的点。

[carla.Client](python_api.md#carla.Client.apply_batch_sync) 中的一个片段使用批次生成大量行人并让它们四处游荡。

!!! 重要
    __要销毁人工智能行人__，请停止人工智能控制器并销毁参与者和控制器。

---
关于 Carla 中的参与者，这就是一个总结。下一步将仔细研究 Carla 的地图、道路和交通。

继续阅读以了解更多信息，或访问论坛发布在阅读过程中想到的任何疑问或建议。
<div text-align: center>
<div class="build-buttons">
<p>
<a href="https://github.com/OpenHUTB/doc/issues" target="_blank" class="btn btn-neutral" title="CARLA forum">
讨论页面</a>
</p>
</div>
<div class="build-buttons">
<p>
<a href="../core_map" target="_blank" class="btn btn-neutral" title="3rd. Maps and navigation">
第三. 地图和导航</a>
</p>
</div>
</div>
