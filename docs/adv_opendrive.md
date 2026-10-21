# OpenDRIVE独立模式

此功能允许用户将任何 OpenDRIVE 文件作为 Carla 地图开箱即用。为此，模拟器将自动生成道路网格供参与者导航。

* [__概述__](#overview)
* [__运行独立地图__](#independent_running_map)
* [__网格生成__](#grid_generation)

---
## 概述 <span id="overview"></span>

此模式仅使用 OpenDRIVE 文件运行完整模拟，无需任何额外的几何图形或资产。为此，模拟器采用 OpenDRIVE 文件并程序化地创建时间三维网格来运行模拟。

生成的网格以简约的方式描述了道路定义。所有元素都将与 OpenDRIVE 文件对应，但除此之外，只有 void。为防止车辆掉出路面，采取了两项措施。

* 在车辆流动最复杂的路口，车道稍宽一些。
* 在道路的边界处创建了可见的墙壁，作为最后的安全措施。

交通信号灯、停车标志和让行标志将即时生成。行人将在地图上显示的人行道和人行横道上导航。所有这些元素，以及道路上的每一个细节，都基于 OpenDRIVE 文件。由于独立模式直接使用 `.xodr`，因此其中的任何问题都会影响到模拟。这可能是一个问题，尤其是在许多车道混合的路口。

!!! 重要的
    仔细检查 OpenDRIVE 文件尤为重要，可以先使用 [bimant](https://opendrive.bimant.com/) 或 [odrviewer](https://odrviewer.io/) 进行初步在线查看。运行模拟时，其中的任何问题都会传播。

![opendrive_standalone](img/opendrive_standalone.jpg)

---
## 运行独立地图 <span id="independent_running_map"></span>

打开 OpenDRIVE 文件只需通过 API 调用 [`client.generate_opendrive_world()`](python_api.md#carla.Client.generate_opendrive_world)。这将生成新地图，并阻止模拟，直到它准备好。该方法需要两个参数。

* __`opendrive`__ 是解析为字符串的 OpenDRIVE 文件的内容。
* __`parameters`__ 是一个 [carla.OpendriveGenerationParameters](python_api.md#carla.OpendriveGenerationParameters) 包含网格生成的设置。 __这个参数是可选的__。

* __`vertex_distance`__ *（默认 2.0 米）* - 网格顶点之间的距离。距离越大，网格越不准确。但是，如果距离太小，生成的网格将太重而无法使用。
* __`max_road_length`__ *（默认 50.0 米）* - 网格的一部分的最大长度。网格被分成几部分以减少渲染开销。如果一部分不可见，UE 将不会渲染它。部分越小，它们被丢弃的可能性就越大。但是，如果部分太小，UE 需要管理的对象太多，性能也会受到影响。
* __`wall_height`__ *（默认为 1.0 米）* - 在道路边界上创建的附加墙的高度。这些可以防止车辆坠入虚空。
* __`additional_width`__ *（默认为 0.6 米，每边 0.3）* — 应用于交叉路口的小宽度增量。这是防止车辆坠落的安全措施。
* __`smooth_junctions`__ *(default True)* — 如果 __True__，OpenDRIVE 的一些信息将被重新解释以平滑连接处的最终网格。这样做是为了防止在不同车道相遇时可能发生的一些不准确。如果设置为 __False__，网格将完全按照 OpenDRIVE 中的描述生成。
* __`enable_mesh_visibility`__ *(default True)* — 如果 __False__，网格将不会被渲染，这可以为模拟器节省大量渲染工作。


为了轻松测试此功能，`PythonAPI/util/` 中的 [config.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/util/config.py) 脚本有一个新参数，`-x` 或`--xodr-path`。此参数需要一个带有 `.xodr` 文件路径的字符串，例如 `path/example.xodr`。如果使用此脚本生成网格，则使用的参数将始终为默认参数。

此功能可以使用 Carla 提供的新 __TownBig__ 进行测试。

```sh
python3 config.py -x opendrive/TownBig.xodr
```


!!! 重要的
    __[client.generate_opendrive_world()](python_api.md#carla.Client.generate_opendrive_world)__ 使用 __OpenDRIVE 文件的内容解析为字符串__ 。相反，__[config.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/util/config.py)__ 脚本需要 __`.xodr` 文件的路径__。

!!! 笔记
如果遇到`opendrive 无法正确解析`错误，请确保对`CarlaUE4/Content/Carla/Maps/OpenDrive/`目录有写权限。这是服务器正确解析`xodr`文件所必需的。

---
## 网格生成 <span id="grid_generation"></span>

网格的生成是该模式的关键要素。只有当生成的网格是平滑的并且完全符合其定义时，该功能才能成功。出于这个原因，这一步正在不断改进。在最后的迭代中，连接点已经过抛光以避免不准确
发生，尤其是在不平坦的车道连接处。

![opendrive_meshissue](img/opendrive_meshissue.jpg)
<div style="text-align: center"><i>在生成岔路口网格时，较高的车道往往会阻挡下方的车道。 <br><code>smooth_junctions</code> 参数可防止此类问题。</i></div>

<br>


除此之外，不是将整个地图创建为一个独特的网格，而是创建不同的部分。通过划分网格，模拟器可以避免渲染不可见的部分，并节省成本。工作更小还允许生成巨大的地图并包含可能出现在网格的一小部分上的问题。

关于网格生成的当前状态，应考虑一些因素。

* __岔路口平滑__。默认平滑可防止上述倾斜连接处的问题。但是，它会在此过程中修改原始网格。如果愿意，将 `smooth_junctions` 设置为 __False__ 以禁用平滑。
* __横向坡度__。此功能当前未集成在 Carla 中。
* __人行道高度__。目前，所有人行道的硬编码都是相同的。人行道必须高于道路标高才能检测到碰撞，但 RoadRunner 不会将此值导出到 OpenDRIVE 文件。高度是硬编码的，以保证碰撞。
---

这涵盖了到目前为止关于 OpenDRIVE 独立模式的所有信息。抓住机会使用任意 OpenDRIVE 地图在 HUTB 中进行测试。

有任何疑问和建议请访问 HUTB 论坛。

<div class="build-buttons">
<p>
<a href="https://github.com/OpenHUTB/hutb/discussions" target="_blank" class="btn btn-neutral" title="前往 HUTB 论坛">
HUTB 论坛</a>
</p>
</div>

