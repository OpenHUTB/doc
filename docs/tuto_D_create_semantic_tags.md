# 创建语义标签

了解如何定义语义分割的自定义标签。这些还可以添加到 [carla.CityObjectLabel](python_api.md#carla.CityObjectLabel) 以过滤 [carla.World](python_api.md#carla.World) 检索的边界框。
 

*   [__创建新的语义标签__](#create-a-new-semantic-tag)  
	*   [1. 创建标签 ID](#1-create-the-tag-id)  
	*   [2. 创建资产的虚幻引擎文件夹](#2-create-the-ue-folder-for-assets)  
	*   [3. 创建虚幻引擎与代码标签的双向对应关系](#3-create-two-way-correspondence-between-ue-and-the-code-tag)  
	*   [4. 定义颜色代码](#4-define-a-color-code)  
	*   [5. 添加标记元素](#5-add-the-tagged-elements)  
*   [__将标签添加到 carla.CityObjectLabel__](#add-a-tag-to-carlacityobjectlabel)  

---

## 创建新的语义标签 <span id="create-a-new-semantic-tag"></span>

### 1. 创建标签 ID <span id="1-create-the-tag-id"></span>

__打开 `LibCarla/source/carla/rpc` 中的 `ObjectLabel.h`__ 。使用与其余标签相同的格式在枚举末尾添加新标签。

![object_label_h](img/tuto_D_create_semantic_tags/01_objectlabel_tag.jpg)

!!! 笔记
    标签不必按顺序出现。但是，按顺序列出它们是一个很好的做法。

### 2. 创建资产的虚幻引擎文件夹 <span id="2-create-the-ue-folder-for-assets"></span>

__打开虚幻引擎编辑器__ 并转到 `Carla/Static`。创建一个名为您的标签的新文件夹。

![ue_folder](img/tuto_D_create_semantic_tags/02_ue_folder.jpg)

!!! 笔记
    虚幻编辑器文件夹和标签不必命名相同。然而，这样做是一个很好的做法。 

### 3. 创建虚幻引擎与代码标签的双向对应关系 <span id="3-create-two-way-correspondence-between-ue-and-the-code-tag"></span>

__3.1. 打开`Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game`中的 `Tagger.cpp`__ 。转到 __`GetLabelByFolderName`__ 列表末尾添加您的标签。被比较的字符串是 [__2.__](#2-create-the-ue-folder-for-assets) 中使用的虚幻引擎文件夹的名称，因此这里使用完全相同的名称。

![tagger_cpp](img/tuto_D_create_semantic_tags/03_tagger_cpp.jpg)

__3.2. 在相同的 `Tagger.cpp` 转到 `GetTagAsString`__ 。 在开关末尾添加新标签。

![tagger_cpp_02](img/tuto_D_create_semantic_tags/04_tagger_cpp_02.jpg)

### 4. 定义颜色代码 <span id="4-define-a-color-code"></span>

__在 `LibCarla/source/carla/image` 中打开 `CityScapesPalette.h`__ 。在数组末尾添加新标签的颜色代码。

![city_scapes_palette_h](img/tuto_D_create_semantic_tags/05_city_scapes_palette_h.jpg)

!!! 笔记
    数组中的位置必须与标签 ID 相对应，在本例中为 `23u`. 

### 5. 添加标记网格 <span id="5-add-the-tagged-elements"></span>

新的语义标签已可供使用。只有存储在标签的虚幻引擎文件夹内的网格才会被标记为此类。将相应的网格移动或导入到新文件夹中，以便正确标记。

---

## 将标签添加到 [carla.CityObjectLabel](python_api.md#carla.CityObjectLabel) <span id="add-a-tag-to-carlacityobjectlabel"></span>

这一步与语义分割没有直接关系。但是，这些标签可用于过滤 [carla.World](python_api.md#carla.World) 中的边界框查询。为此，必须将标签添加到PythonAPI 中的 [carla.CityObjectLabel](python_api.md#carla.CityObjectLabel) 枚举中。


__在 `carla/PythonAPI/carla/source/libcarla` 中打开 `World.cpp`__ 并在枚举末尾添加新标签。

![city_object_label](img/tuto_D_create_semantic_tags/06_city_object_label.jpg)


---

如果有任何问题、疑问或建议，请阅读 **[常见问题解答](build_faq.md)** 页面或在 [OpenHUTB 论坛](https://github.com/OpenHUTB/hutb/discussions) 中发帖。


<div class="build-buttons">

<p>
<a href="../ref_sensors" target="_blank" class="btn btn-neutral" title="Learn all about sensors in CARLA">
传感器参考</a>
</p>

<p>
<a href="../tuto_A_add_props" target="_blank" class="btn btn-neutral" title="Learn how to import your custom into HUTB">
添加新道具</a>
</p>

</div>
