# [第三、地图和导航](https://carla.readthedocs.io/en/latest/core_map/) 

在讨论了世界及其参与者之后，是时候将所有内容都放在适当的位置并了解地图以及参与者如何导航。

- [__地图__](#the-map)  
    - [改变地图](#changing-the-map)  
    - [地标](#landmarks)  
    - [路径点](#waypoint)  
    - [车道](#lanes)  
    - [路口](#junctions)
    - [环境对象](#environment-objects)
- [__在 Carla 中导航__](#navigation-in-carla)  
    - [通过路径点导航](#navigating-through-waypoints)  
    - [生成地图导航](#generating-a-map-navigation)  
- [__Carla 地图__](#carla-maps)  
    - [非分层地图](#non-layered-maps)
    - [分层地图](#layered-maps)
- [__自定义地图__](#custom-maps)
    - [概述](tuto_M_custom_map_overview.md)
    - [道路涂装 painting](tuto_M_custom_road_painter.md)
    - [定制建筑](tuto_M_custom_buildings.md) 
    - [生成地图](tuto_M_generate_map.md)
    - [添加地图包](tuto_M_add_map_package.md)
    - [添加地图源](tuto_M_add_map_source.md)
    - [替代方法](tuto_M_add_map_alternative.md)
- [__靠左行驶的交通__](#left-handed-traffic)
- [__附加地图__](#additional-maps)


---
## 地图 <span id="the-map"></span>

地图包括城镇的三维模型及其道路定义。地图的道路定义基于 OpenDRIVE 文件，这是一种标准化的带注释的道路定义格式。[OpenDRIVE 1.4 标准](http://www.opendrive.org/docs/OpenDRIVEFormatSpecRev1.4H.pdf) 定义道路、车道、路口等方式决定了 Python API 的功能以及决策背后的推理。

Python API 充当高级查询系统来导航这些道路。它不断发展以提供更广泛的工具集。


### 改变地图 <span id="changing-the-map"></span>

__要改变地图，世界也必须改变__。将从头开始重新创建模拟。您可以在新世界中使用相同的地图重新启动，也可以更改地图和世界：

- `reload_world()` 使用相同的地图创建世界的新实例。
- `load_world()` 改变当前地图并创建一个新世界。

```py
world = client.load_world('Town01')
```

每个地图都有一个与当前加载的城市名称匹配的`name`属性，例如 _Town01_ 。要获取可用地图的列表：

```py
print(client.get_available_maps())
```

### 地标 <span id="landmarks"></span>

OpenDRIVE 文件中定义的交通标志将转换为 Carla，作为可从 API 查询的地标对象。以下方法和类可用于操作和使用地标对象：

- __[`carla.Landmark`](python_api.md#carla.Landmark)__ 对象代表 OpenDRIVE 信号。该类的属性和方法描述了地标及其影响区域。
	- [`carla.LandmarkOrientation`](https://carla.readthedocs.io/en/latest/python_api/#carla.LandmarkOrientation) 说明地标相对于道路几何定义的方向。
	- [`carla.LandmarkType`](https://carla.readthedocs.io/en/latest/python_api/#carla.LandmarkType) 包含常见的地标类型，以便于转换为 OpenDRIVE 类型。
- __[`carla.Waypoint`](https://carla.readthedocs.io/en/latest/python_api/#carla.Waypoint)__ 可以获得位于其前方一定距离的地标。可以指定要获取的地标类型。
- __[`carla.Map`](https://carla.readthedocs.io/en/latest/python_api/#carla.Map)__ 检索地标集。它可以返回地图中的所有地标，或者具有共同 ID、类型或组的地标。
- __[`carla.World`](https://carla.readthedocs.io/en/latest/python_api/#carla.World)__ 充当地标、模拟中代表他们的`carla.TrafficSign` 和 `carla.TrafficLight` 之间的中间。

```py
my_waypoint.get_landmarks(200.0,True)
``` 

### 路径点 <span id="waypoint"></span>

[`carla.Waypoint`](python_api.md#carla.Waypoint) 是 Carla 世界中的三维有向点，对应于 OpenDRIVE 车道。与路径点相关的所有事情都发生在客户端；只需与服务器通信一次即可获取包含路径点信息的[地图对象](python_api.md#carlamap)。

每个路径点都包含一个 [`carla.Transform`](python_api.md#carla.Transform) ，它说明其在地图上的位置以及包含该路径点的车道的方向。变量`road_id`,`section_id`,`lane_id` 和 `s`对应 OpenDRIVE 道路。路径点`id`的是由这四个值的哈希组合构造的。


!!! 笔记
    __同一道路内距离小于 2 厘米__ 的路点共享相同的路点 `id`。

路径点保存有关包含该路径点的 __车道__ 的信息。此信息包括车道的左车道和右 __车道标记__、用于确定其是否位于路口内的布尔值、车道类型、宽度和车道变更权限。

```py
# 从路径点访问车道信息
inside_junction = waypoint.is_junction()
width = waypoint.lane_width
right_lm_color = waypoint.right_lane_marking.color
```

### 车道 <span id="lanes"></span>


[OpenDRIVE 1.4 标准](http://www.opendrive.org/docs/OpenDRIVEFormatSpecRev1.4H.pdf) 定义的通道类型将 [carla.LaneType](python_api.md#carla.LaneType) 作为一系列枚举值转换为 API 。


车道周围的车道标记可通过 [`carla.LaneMarking`](python_api.md#carla.LaneMarking) 访问。车道标记由一系列变量定义：

- __color:__ [`carla.LaneMarkingColor`](python_api.md#carla.LaneMarkingColor) 是定义标记颜色的枚举值。
- __lane_change:__ [`carla.LaneChange`](python_api.md#carla.LaneChange) 说明车道是否允许左转、右转、两者都允许或不允许。
- __type:__ [`carla.LaneMarkingType`](python_api.md#carla.LaneMarkingType) 是根据 OpenDRIVE 标准定义标记类型的枚举值。
- __width:__ 定义标记的厚度。

下面的示例显示了获取有关特定路径点的车道类型、车道标记和车道变更权限的信息：

```py
# 获得路径点车道类型
lane_type = waypoint.lane_type

# 获得左车道标记的类型
left_lanemarking_type = waypoint.left_lane_marking.type()

# 获得该路径点可得的车道改变
lane_change = waypoint.lane_change
```

### 路口 <span id="junctions"></span>

[`carla.Junction`](python_api.md#carla.Junction) 代表 OpenDRIVE 连接点。此类包含带有边界框的交汇处，用于识别其中的车道或车辆。

该 `carla.Junction` 类包含 `get_waypoints` 为交汇处的每个车道返回一对路点的方法。每对位于交界处边界的起点和终点。

```py
waypoints_junc = my_junction.get_waypoints()
```

### 环境对象 <span id="environment-objects"></span>

Carla 地图上的每个对象都有一组关联的变量，可以在 [此][env_obj] 处找到这些变量。这些变量中包含一个 [唯一 ID][env_obj_id]，可用于切换该对象在地图上的可见性。您可以使用 Python API 根据每个环境对象的[语义标签]([semantic_tag]) [获取][fetch_env_obj] 其 ID ：

	# 获得世界中的建筑
	world = client.get_world()
	env_objs = world.get_environment_objects(carla.CityObjectLabel.Buildings)

	# 访问各个建筑 IDs 并保存在集合当中
	building_01 = env_objs[0]
	building_02 = env_objs[1]
	objects_to_toggle = {building_01.id, building_02.id}

	# 切换建筑为不可见
	world.enable_environment_objects(objects_to_toggle, False)
	# 切换建筑为可见
	world.enable_environment_objects(objects_to_toggle, True)

查看切换不同对象的示例：

![toggle_objects_gif](img/objects_small.gif)

[env_obj]: https://carla.readthedocs.io/en/latest/python_api/#carla.EnvironmentObject
[env_obj_id]: https://carla.readthedocs.io/en/latest/python_api/#carla.EnvironmentObject.id
[toggle_env_obj]: https://carla.readthedocs.io/en/latest/python_api/#carla.World.enable_environment_objects
[fetch_env_obj]: https://carla.readthedocs.io/en/latest/python_api/#carla.World.get_environment_objects
[semantic_tag]: https://carla.readthedocs.io/en/latest/python_api/#carla.CityObjectLabel


---
## 在 Carla 中导航 <span id="navigation-in-carla"></span>

Carla 中的导航是通过 Waypoint API （来自 [`carla.Waypoint`](python_api.md#carla.Waypoint) 和 [`carla.Map`](python_api.md#carla.Map) 的方法组合）进行管理。

客户端必须首先与服务器通信以检索包含路径点信息的地图对象。这只需要一次，所有后续查询都在客户端执行。


### 通过路径点导航 <span id="navigating-through-waypoints"></span>

Waypoint API 公开了允许路径点相互连接并构建沿道路供车辆导航的路径的方法：

- `next(d)`  __在车道方向上__ 创建近似距离 `d` 内的路径点列表。该列表包含每个可能偏差的一个路径点。
- `previous(d)` __在车道相反的方向上__ 创建近似距离小于 `d` 的路径点列表。该列表包含每个可能偏差的一个路径点。
- `next_until_lane_end(d)` 和 `previous_until_lane_start(d)` 返回相距一定距离 `d` 的路径点列表。这些列表分别从当前路径点到其车道的终点和起点。
- `get_right_lane()` 和 `get_left_lane()` 返回相邻车道中的等路径点（如果存在）。可以通过找到右/左车道上的下一个路点并移动到该路点来进行变道操作。

```py
# 找到前面 2 米的下一个路径点
waypoint = waypoint.next(2.0)
```

### 生成地图导航 <span id="generating-a-map-navigation"></span>

客户端需要向服务器发出请求来获取 <font color="#f8805a">.xodr</font> 地图文件并将其解析为[`carla.Map`](python_api.md#carla.Map) 对象。这只需要做一次。

获取地图对象：

```py
map = world.get_map()
```

地图对象包含用于创建车辆的 __推荐生成点__。您可以使用以下方法获取这些生成点的列表，每个生成点都包含 [`carla.Transform`](python_api.md#carlatransform)。请记住，生成点可能已被占用，从而导致由于碰撞而导致车辆创建失败。


```py
spawn_points = world.get_map().get_spawn_points()
```

您可以通过[获取](python_api.md#carla.Map.get_waypoint)距特定位置或特定 `road_id`、`lane_id`和`s`位置最近的路径点以及地图 OpenDRIVE 定义中的值来开始使用路径点：

```py
# 驾驶车道或人行道中心最近的路径点。
waypoint01 = map.get_waypoint(vehicle.get_location(),project_to_road=True, lane_type=(carla.LaneType.Driving | carla.LaneType.Sidewalk))

# 最近的路径点，同时指定 OpenDRIVE 参数。
waypoint02 = map.get_waypoint_xodr(road_id,lane_id,s)
```

下面的示例展示了如何 __生成路点集合__ 以可视化城市车道。这将为整个地图上的每条道路和车道创建路径点。它们之间的距离大约为 2 米：

```py
waypoint_list = map.generate_waypoints(2.0)
```

要 __生成道路拓扑的最小图__，请使用下面的示例。这将返回路径点对（元组）的列表。每对中的第一个元素与第二个元素连接，两者都定义了地图中每条车道的起点和终点。有关此方法的更多信息可以在[PythonAPI](python_api.md#carla.Map.get_topology)中找到。

```py
waypoint_tuple_list = map.get_topology()
```

下面的示例 __将 `carla.Transform` 转换为地理纬度和经度坐标__，采用 [`carla.GeoLocation`](python_api.md#carla.GeoLocation) 的形式：

```py
my_geolocation = map.transform_to_geolocation(vehicle.transform)
```

使用以下示例将 OpenDRIVE 格式的 __道路信息保存到磁盘__：

```py
info_map = map.to_opendrive()
```

---
## Carla 地图 <span id="carla-maps"></span>

Carla 生态系统中有八个城镇，每个城镇都有两种地图，非分层地图和分层地图。[图层][layer_api]是指地图中分组的对象，由以下部分组成：

- NONE
- 建筑物
- 贴标
- 叶子
- 地面
- 停放的车辆
- 粒子
- 道具
- 路灯
- 墙壁
- 全部

[layer_api]: https://carla.readthedocs.io/en/latest/python_api/#carlamaplayer

### 非分层地图 <span id="non-layered-maps"></span>

下表显示了非分层地图（单击城镇名称可查看布局的俯视图）。所有图层始终存在，并且无法在这些地图中打开或关闭。直到 Carla 0.9.11 为止，这些是唯一可用的地图类型。

!!! 笔记
    用户可以使用 [自定义地图](tuto_A_map_customization.md) 甚至创建要在 Carla 中使用的 [新地图](tuto_M_custom_map_overview.md)。

| 城镇                                                                    | 概括                                                                                                                                                                                                                        |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **[Town01](img/Town01.jpg)**                                          | 由“T 字路口”组成的基本城镇布局。                                                                                                                                                                                                        |
| **[Town02](img/Town02.jpg)**                                          | 和 **Town01** 类似，但是更小。                                                                                                                                                                                                     |
| **[Town03](img/Town03.jpg)**                                          | 最复杂的城镇，有 5 车道交叉路口、环岛、凹凸不平、隧道等。                                                                                                                                                                                            |
| **[Town04](img/Town04.jpg)**                                          | 有高速公路和小镇的无限循环。                                                                                                                                                                                                            |
| **[Town05](img/Town05.jpg)**                                          | 方形网格城镇，有十字路口和一座桥梁。每个方向有多个车道。对于执行变道很有用。                                                                                                                                                                                    |
| **[Town06](img/Town06.jpg)**                                          | 高速公路长，有许多高速公路入口和出口。它还有一个 [**密歇根左转**](<https://en.wikipedia.org/wiki/Michigan_left>)。                                                                                                                                      |
| **[Town07](img/Town07.jpg)**                                          | 乡村环境，道路狭窄，谷仓，几乎没有交通信号灯。                                                                                                                                                                                                   |
| **[Town10](img/Town10.jpg)**                                          | 具有大道或长廊等不同环境的城市环境，以及更真实的纹理（[UE5 Town10](https://pan.baidu.com/s/1q96tyOIMJjpCw5KwL0qnsQ?pwd=hutb) `car/Carla_UE5/Carla_UE5_Windows.exe.zip`）。                                                                             |
| **[Town11](map_town11.md)**                                           | 具有大道或长廊等不同环境的城市环境，以及更真实的纹理。                                                                                                                                                                                               |
| **[Town12](map_town12.md)**                                           | 一张包含许多不同区域的大地图，包括高层建筑、住宅区和乡村环境。                                                                                                                                                                                           |
| [__Town13__](map_town13.md)                                           | 一张与 12 号镇规模相似的大地图，但具有鲜明的特色。                                                                                                                                                                                               |
| [__Town15__](map_town15.md)                                           | 基于巴塞罗那自治大学道路布局的地图。                                                                                                                                                                                                        |
| [__湖南工商大学__]([链接](https://pan.baidu.com/s/1n2fJvWff4pbtMe97GOqtvQ?pwd=hutb))  | 基于湖南工商大学道路布局的地图（可执行场景位于 [链接](https://pan.baidu.com/s/1n2fJvWff4pbtMe97GOqtvQ?pwd=hutb) 中的`software/car/湖南工商大学.zip`，其资产位于 [链接](https://bitbucket.org/hutbcity/openhutbcarla/src/main/) ，[导入方法](tutorial/import_HUTB.md) ）。 |
| [__中电软件园__](https://pan.baidu.com/s/1q96tyOIMJjpCw5KwL0qnsQ?pwd=hutb) | 基于长沙市中电软件园（Changsha CEC Software Park, CCSP）道路布局的地图（位于`car/中电软件园/WindowsNoEditor.zip`，资产位于`D:\model1\model1\tileset.json`）。                                                                                               |

!!! 注意
	Town06 和 Town07 是附加内容，不包含在标准 CARLA 包中。请参阅 [附加地图部分](#additional-maps) ，了解如何导入这些内容。


### 分层地图 <span id="layered-maps"></span>

分层地图的布局与非分层地图相同，但可以关闭和打开地图的图层。有一个无法关闭的最小布局，由道路、人行道、交通信号灯和交通标志组成。分层地图可以通过后缀 `_Opt` 来标识，例如`Town01_Opt`。使用这些地图，可以通过 Python API [加载][load_layer]和[卸载][unload_layer]图层：

	# 加载 城镇01 的分层地图，带有最小布局加上建筑物和停放的车辆
	world = client.load_world('Town01_Opt', carla.MapLayer.Buildings | carla.MapLayer.ParkedVehicles)

	# 关闭所有建筑
	world.unload_map_layer(carla.MapLayer.Buildings)

	# 打开所有建筑	
	world.load_map_layer(carla.MapLayer.Buildings)

[load_layer]: https://carla.readthedocs.io/en/latest/python_api/#carla.World.load_map_layer
[unload_layer]: https://carla.readthedocs.io/en/latest/python_api/#carla.World.unload_map_layer

查看按顺序加载和卸载所有层的示例：

![map-layers](img/sublevels.gif)


---

## 自定义地图  <span id="custom-maps"></span>

Carla 旨在针对专业应用程序进行可扩展和高度定制。因此，除了 Carla 中现有的许多地图和资产之外，还可以创建和导入新的地图、道路网络和资产，以填充 Carla 模拟中的定制环境。以下文档详细介绍了构建和集成自定义地图所需的步骤：

* [__概述__](tuto_M_custom_map_overview.md)
* [__道路涂装__](tuto_M_custom_road_painter.md)
* [__定制建筑__](tuto_M_custom_buildings.md) 
* [__生成地图__](tuto_M_generate_map.md)
* [__添加地图包__](tuto_M_add_map_package.md)
* [__添加地图源__](tuto_M_add_map_source.md)
* [__替代方法__](tuto_M_add_map_alternative.md)

## 靠左行驶的交通

CARLA 支持 OpenDRIVE 文件中定义的**靠左行驶的交通**(left-handed traffic, LHT)规则。要在任何道路上调用靠左行驶交通规则，请像这样在 OpenDRIVE XML 文件中应用左侧通行属性：

```xml
<road name="Road 0" length="1.3310253693587601e+1" id="0" junction="-1" rule="LHT">
    <link>
        <predecessor elementType="road" elementId="3" contactPoint="end" />
        <successor elementType="road" elementId="10" contactPoint="start" />
    </link>
...
</road>
```

!!! 注意
	靠右行驶交通惯例为默认规则。没有规则`rule`属性（或包含无法识别的参数）的道路将被视为靠右行驶的道路。您也可以通过添加 `rule="RHT"` 来明确设置靠右行驶规则。

CARLA 将对每条道路应用靠左行驶的交通惯例，并应用 `rule="LHT"` 属性。


请注意，靠左或靠右行驶交通惯例不仅会影响交通行为，还会影响道路的交通标志和信号。因此，如果地图中手动放置了针对靠右行驶的交通惯例的资源（例如道路标志或交通信号灯），则需要进行调整。OpenDRIVE 定义中针对左侧交通定义的交通信号灯将在导入地图后由 CARLA 自动放置在适当的位置。


## 附加地图

每个发行版都有自己的附加包，其中包含额外的资产和地图。此附加包包含地图 __Town06__ 和 __Town07__。为了减小构建文件的大小，这些地图会单独存储，因此只有在安装主包后才能导入。

__1.__ [下载](https://github.com/carla-simulator/carla/blob/master/Docs/download.md) 适合您所需 CARLA 版本的软件包。 

__2.__ 解压包：

- __在 Linux 上__:

    - 将包移动到 _Import_ 文件夹并运行以下脚本来提取内容： 

```sh
cd path/to/carla/root
./ImportAssets.sh
```

- __在 Windows 上__:

    - 直接在根文件夹中提取内容。

---

## 工具

* [webp转gif](https://cloudconvert.com/webp-to-gif)
* [gif压缩](https://gifcompressor.com/zh/)
