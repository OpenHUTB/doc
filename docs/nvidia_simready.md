# [NVIDIA SimReady](https://openhutb.github.io/hutb/nvidia_simready/)

**SimReady** 是一项标准规范，针对的是旨在用于仿真环境的 3D 资产所关联的信息及元数据。SimReady 标准确保 3D 资产不仅是数字孪生中的高保真视觉资源，而且还具有组织良好的元数据定义，包括语义标记、密集字幕、非视觉传感器信息和物理属性。



* __[SimReady 转换器](#simready-converter)__  
* __[使用 SimReady 转换器导出 SimReady 资产](#exporting-an-asset-with-the-simready-converter)__
    * [导出地图](#exporting-a-map)
    * [导出车辆或行人](#exporting-a-vehicle-or-a-pedestrian)
* __[SimReady 导出选项](#simready-export-options)__
* __[语义标签和 Q 码](#semantic-labels-and-q-codes)__

## SimReady 转换器

NVIDIA SimReady 转换器使 Carla 资产能够以符合 SimReady 标准的方式导出为通用场景描述 （Universal Scene Description, USD） 格式，从而便于将其导入到 OmniVerse 生态系统中的其他应用程序（如 Sensor RTX 或 RTX 渲染器）内，以进行联合仿真。


SimReady 转换器在可能的情况下将虚幻对象、属性和参数映射到符合 USD/SimReady 的等效项，并应用适当的元数据（例如语义标签）用于模拟目的。


### 使用 SimReady 转换器导出 SimReady 资产

#### 导出地图

要导出地图，请在 Carla 内容浏览器(content browser) 中找到相应的地图文件。例如，`Content > Carla > Maps`中的 *Town10HD_Opt*。


![map_asset](img/nvidia/map_file.png)

在内容浏览器中双击地图资产以加载它。选择`File > Export All`。将`Save as type`设置为 *AV Sim 的通用场景描述二进制 SimReady 资产 (\*.usd)*。


![export_simready_map](img/nvidia/export_simready_map.png)

选择资产的文件夹位置。单击 *保存(Save)* 选项后，将出现一个选项对话框。在大多数情况下，使用默认选项导出将有效。有关导出选项的更多详细信息，请参阅 [SimReady 选项](#simready-export-options) 部分。


![options_simready_map](img/nvidia/simready_export_options_map.png)

#### 导出车辆或行人

要导出车辆或行人，请找到蓝图文件。例如，`Content >  Carla > Blueprints > Vehicles > Ford_Crown`中的 *BP_Ford_Crown*  或 `Content > Carla > Blueprints > Walkers` 中的 *BP_Walker*。右键单击蓝图并选择 *导出为 USD(Export as USD)*。


![vehicle_bp](img/nvidia/bp_simready_export.png)

将打开一个文件浏览器，为导出的 USD 文件选择一个位置。选择 *保存(Save)* 后，将打开一个选项对话框。默认选项适用于大多数情况。


![bp_export_options](img/nvidia/simready_bp_export_options.png)

有关 SimReady 导出选项的更多详细信息，请参阅以下部分。


## SimReady 导出选项

两个最重要的选项如下：

* `Include MDL` - 选择此选项会将虚幻材质转换为 MDL 材质。确保您要导出的应用程序与 MDL 材质兼容。Omniverse Kit 应用程序与 MDL 材料兼容。

* `Include USD Preview Surface` - 选择此选项会导出带有 USD 预览表面的 USD，这可确保可视化的更广泛兼容性，但材质功能集更有限。这有助于确保在不支持完整 MDL 规范的应用程序中可以正确查看资产。

下表提供了有关可用导出选项的详细信息。更多详细信息可以在 Omniverse Connect 文档中找到 [点击此处](https://docs.omniverse.nvidia.com/connect/latest/ue4/manual.html#exporting-to-omniverse-as-usd-and-mdl) 。


| 选项                                                            | 结果                                                                                                                                                                                                                                                  | 
|---------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Export Method                                                 | 共享（Shared） 组织材质，以便它们可以由许多资源共享\n模块化（Modular） 为<br>每个资源导出一个材质，以便资源及其材质都是独立的 | 
| Include MDL                                                   | 导出 MDL 材料 
| MDL Dependency Option                                         | 包含依赖项 - 在目标文件夹中复制 MDL 依赖项（模板）。使用核心库依赖项 - 引用核心 MDL 库模板。                                                                               | 
| Destination Unreal Template Path                              | Omniverse Nucleus 上用于存放 MDL 依赖项（模板）的目标文件夹<br> 注意：必须选中一个文件，但实际仅使用该文件所在的文件夹                                                                                                         |
| Texture Size                                                  | 使用纹理设置或源文件作为导出纹理尺寸                                                                                                                                                                                              |
| Export Texture as DDS                                         | 将 DDS 文件保存至目标路径，并在材质中进行引用                                                                                                                                                                                |
| Include USD Preview Surface                                   | 导出预览曲面                                                                                                                                                                                                                             |
| Include Unreal Materials                                      | 导出对 Unreal 材质的引用（注意：在导入或打开时，该材质必须已存在于 Unreal 项目中）                                                                                                         |
| Create a material overrides layer                             | 导出一个包含场景中所有材质引用覆盖（material reference overrides）的子层。 <br> 此外，为每种材质分别创建 USD 文件，而不是将其包含在道具场景（prop stages）中。                                                                      |
| Export physics data                                           | 在静态网格体中包含碰撞数据（由于 USD 架构更新，此功能在 Unreal Engine 5.0 中不可用）                                                                                                                                          |
| Export source geometry for<br> Nanite high-poly detailed mesh | 以“暴力”方式将 Nanite 几何体导出为 USD 几何数据。 <br> （仅适用于 Unreal Engine 5.0；此操作会生成海量的三角形）                                                                                                         |
| USD Scenegraph Instancing                                     | 将场景（Stage）中所有被引用的网格（Mesh）设为实例（Instance）。如果场景中存在重复的网格，此操作可在其他渲染器中大幅减少几何数据占用的 GPU 显存，但可能会对编辑工作流程造成阻碍。                                            |
| Export as Payloads                                            | 在 stage 中使用载荷（payloads）而非引用（references）                                                                                                                                                                                                     |
| Export as Y-up axis                                           | 若勾选此项，在导出 USD 和 MDL 文件时，场景向上轴（stage up-axis）将设为 Y 轴向上，而非默认的 Z 轴向上。                                                                                                                                                     |
| Export Sublevels as Sublayers                                 | 如果勾选此项，层级将作为 USD 子层导出，<br> 并在根阶段（root stage）中进行引用。                                                                                                                                                               |
| Convert Skeleton root to identity transform                   | 此选项会将骨架的根节点转换为单位变换（identity transform），以支持有此要求的后续工具。在此次导出过程中，所有导出的动画都将经过相应变换，确保其能够在后续工具中正常使用。         |
| Include invisible levels                                      | 如果勾选此项，处于隐藏状态的层级将包含在导出内容中，并被标记为不可见。                                                                                                                                                       |
| Export Decal Actors as planes                                 | 若勾选此项，贴花 Actor 将被导出为“悬浮（floating）”的平面网格体，并与各自的基准网格体保持一定偏移。                                                                                                                                                    |
| Add extra extension to exports                                | Stage 文件将命名为 `.stage.usd`，道具（props）将命名为 `.prop.usd`。                                                                                                                                                                              |
| Checkpoint Comment (Optional)                                 | 为每个导出的文件在 Nucleus 服务器上设置检查点注释                                                                                                                                                                             |

## 语义标签和 Q代码

SimReady 标准使用 [Q 代码](https://en.wikipedia.org/wiki/Q_code) 进行语义标记。Q 代码是三个字母代码的标准化集合，这些代码都以字母 Q 开头。SimReady 导出器为从 Carla 导出的每个语义标记项应用适当的 Q 代码，作为 USD 文件中对象元数据的一部分。您可以在 [维基数据网站](https://www.wikidata.org/wiki/Wikidata:Main_Page) 上查找 Q 代码定义。



下表显示了 Carla 语义类到 Q 码的映射：


| 标签 | Q 码 |
|-------|--------|
| 道路（Road） | Q34442 |
| 人行道（SideWalk） | Q177749 |
| 建筑物（Building） | Q41176 |
| 墙（Wall） | Q42948 |
| 围栏（Fence） | Q148571 |
| 杆状物（Pole） | Q2180428 |
| 交通信号灯（TrafficLight） | Q8004 |
| 交通标志（TrafficSign） | Q170285 |
| 植被（Vegetation） | Q187997 |
| 地形（Terrain） | Q186131 |
| 天空（Sky） | Q527 |
| 行人（Pedestrian） | Q221488 |
| 骑行者（Rider） | Q11998775 |
| 小客车（Car） | Q1420 |
| 卡车（Truck） | Q43193 |
| 公交车（Bus） | Q5638 |
| 火车（Train） | Q870 |
| 摩托车（Motorcycle） | Q34493 |
| 自行车（Bicycle） | Q11442 |
| 静态（Static） | Q2302426 |
| 动态（Dynamic） | Q2302426 |
| 其他（Other） | Q55107540 |
| 水体（Water） | Q283 |
| 道路标线（RoadLine） | Q1392287 |
| 地面（Ground） | Q36133 |
| 桥梁（Bridge） | Q12280 |
| 铁轨（RailTrack） | Q57498564 |
| 护栏（GuardRail） | Q1188866 |


你好
## 总结

从地图到车辆行人，从导出选项到 Q 码语义映射，SimReady 转换器为虚幻引擎资产打开了一条通往标准化仿真的高效通道。合理利用 MDL 材质、USD 预览表面、Payload 导出等选项，并准确应用 Q 码标签，你的数字孪生场景就能在 Sensor RTX、RTX 渲染器等协作模拟环境中发挥更大价值。不妨打开 Carla 内容浏览器，从导出第一张 SimReady 地图开始，让资产真正“可仿真、可理解、可复用”。





