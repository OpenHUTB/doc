# `DReyeVR` 开发

对于想要深入了解 DReyeVR 内部运作原理以及如何开始开发和编写代码的用户来说，无需再四处寻找了！

（本指南假设您已阅读 [`Usage.md`](../Usage.md) 文档并已安装 `DReyeVR` ）。

# 入门

我们建议您采用一种开发环境，以便能够快速识别您对 DReyeVR 的更改与上游更改之间的差异。为此，我们提供了一个预装（并已提交）DReyeVR 的 CARLA 分支，这样您就可以使用一个干净的初始代码库：
```bash
# 克隆我们的分支并替换你原有的 CARLA 仓库。
git clone https://github.com/harplab/carla -b DReyeVR-0.9.13 --depth 1
cd carla
# ./Update.sh # 在 Linux/Mac 系统中
Update.bat # 在 Windows 系统中

cd ../DReyeVR/ # 假设 DReyeVR 代码库与 carla 代码库相邻。

# (在 DReyeVR 仓库)
make install CARLA=../carla # 安装未被 Git 跟踪的内容，例如蓝图/二进制文件

cd ../carla # 切换回 carla 目录
git status
# 现在，git 应该显示相对于我们上游 DReyeVR 分支的更改，而不是相对于 CARLA 0.9.13 分支的更改。
```

## 反向安装

一旦您对 Carla 代码库中与 DReyeVR 相关的部分进行了更改，手动将所有这些更改复制回 DReyeVR 代码库（如果您想将其提交到上游）将非常繁琐。作为我们构建系统的一部分，我们提供了一个“反向安装”（r-install）**工具**，用于镜像安装 `install` 功能，并将 DReyeVR（通过 `make install`）安装的所有相应文件复制回 DReyeVR：

<details>

<summary> 点击打开示例以生成输出</summary>

```bash
make r-install CARLA=../carla # 相当于 "make rev"
make rev CARLA=../carla       # r-install 的别名

Proceeding on /PATH/TO/CARLA (git branch)
/PATH/TO/CARLA/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/ -- found
/PATH/TO/CARLA/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoVehicle.h -- found
/PATH/TO/CARLA/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoVehicle.h -> /Users/gustavo/carla/DReyeVR-Dev/DReyeVR/EgoVehicle.h
/PATH/TO/CARLA/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/FlatHUD.cpp -- found
/PATH/TO/CARLA/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/FlatHUD.cpp -> /Users/gustavo/carla/DReyeVR-Dev/DReyeVR/FlatHUD.cpp
...etc.
...
Done Reverse Install!
```
</details>
<br>

请注意，复制回 DReyeVR 的文件遵循 [`Paths/*.csv`](../Scripts/Paths/) 中定义的 DReyeVR <--> Carla 文件对应关系，因此，如果您修改了一个全新的文件（DReyeVR 未跟踪的文件），则需要手动将该文件添加到 DReyeVR 存储库并更新对应关系文件 (.csv)。

## 典型工作流程

我们在 DReyeVR 上设计的开发流程包括使用我们 fork 的 carla（`DReyeVR-0.9.13` 分支）以及一个克隆的 `DReyeVR` 仓库，我们可以使用该仓库从上游推送和拉取代码。

<details>

<summary>点击打开终端命令示例</summary>

```bash
> ls
carla.harp/    # 我们为主要开发项目创建了 HarpLab 分支
DReyeVR        # 我们的 DReyeVR 安装

cd carla.harp
... # 对 carla.harp 进行一些更改
make launch && make package # 确保 carla 在这些变化后仍然能够正常工作

cd ../DReyeVR
make rev CARLA=../carla.harp # "reverse-install" changes from carla.harp to DReyeVR
git stuff # do all sorts of upstreaming and whatnot.

----------------- # 如果上游已进行更改，则需要您进行安装。
cd DReyeVR/
git pull # 上游变化
make clean CARLA=../carla.harp   # （可选）将 carla.harp 重置为干净的 git 状态
make install CARLA=../carla.harp # 安装新的 DReyeVR 更改
cd ../carla.harp && make launch && make package && etc.

# 您也可以选择保留一个 carla.vanilla 文件，以便测试您更新后的 DReyeVR 仓库的全新安装是否能在 carla 上运行。
make install CARLA=../carla.vanilla
```

</details>
<br>

![Directories](Figures/Dev/Directories.jpg)

# 了解 Carla + DReyeVR 代码库的位置

在 Carla 上进行开发时，您需要重点关注以下几个方面：

1. `Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/`
    - 这包含了我们所有的自定义 DReyeVR C++ 代码，这些代码通常是在现有的 Carla 代码基础上构建的。
2. `Unreal/CarlaUE4/Plugins/Carla/Source/Carla/`
    - 这里定义了 UE4 C++ Carla 的主要逻辑，涵盖了从传感器到车辆，再到记录器/回放器和天气等所有内容。
    - 这里有一些代码，例如用于自定义传感器和小功能补丁的代码。
3. `LibCarla/source/carla/`
    - 这里存放了几乎所有与 `Python` 交互的 Carla C++ 代码。其中大部分是对 `CarlaUE4/Plugins` 代码的重新实现，但没有使用 Unreal C++ API，并且非常注重向 Python API 传输数据流逻辑。
    - 这里有一小段代码，用于确保传感器数据能够正确地传输到 Python。
4. `PythonAPI/examples/`
    - 在这里您可以找到与 Carla 交互的大部分重要 Python 脚本。
    - 这里有一些文件，用于改善 DReyeVR 和 Carla 的 PythonAPI 的使用体验。


# 内部运作

本节将讨论 DReyeVR 的内部运作，包括设计范式以及与 Carla 的相应握手。

## EgoVehicle
- 相关文件： [EgoVehicle.h](../DReyeVR/EgoVehicle.h), [EgoVehicle.cpp](../DReyeVR/EgoVehicle.cpp), [EgoInputs.cpp](../DReyeVR/EgoInputs.cpp), [Content/DReyeVR/EgoVehicle/BP_*.uasset](../Content/DReyeVR/EgoVehicle/)

EgoVehicle 是我们的“英雄车”，也是我们的主要载体。为了提升 Carla 中人类驾驶员的沉浸感，EgoVehicle 包含许多普通 Carla 车辆所不具备的以人为中心的功能。例如，EgoVehicle 定义了车内后视镜、动态方向盘、仪表盘、人为输入、音频等的逻辑。这些都是人工智能车辆无需关注的功能，因此 Carla 在其他所有车辆中都省略了这些功能。


不过，EgoVehicle 只是标准 [`ACarlaWheeledVehicle`](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vehicle/CarlaWheeledVehicle.h) 的一个封装（子类），因此它会自动继承所有 Carla 车辆操作，并兼容所有 CarlaVehicle 功能。值得注意的是，EgoVehicle 并非由玩家拥有，而是由默认的 [`AWheeledVehicleAIController`](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vehicle/WheeledVehicleAIController.h) 拥有。这样做是为了允许玩家和内置的 Carla 自动驾驶系统同时进行输入。我们将在下文的 `DReyeVRPawn` 部分对此进行更详细的讨论。

重要的是，我们所有的节拍同步逻辑都基于 EgoVehicle，其 `Tick` 方法会调用 DReyeVR 中许多其他关键组件的 `Tick` 方法。这确保了模拟器中更新的顺序是确定且一致的，并且将来可以依赖这种顺序。

在这里，我们也手动管理 EgoVehicle 的回放行为，它会遵循从 EgoSensor 捕获的值，而不是 Carla 的默认行为，这样我们就可以更精确地重现从 EgoSensor 收集的确切数据，例如眼睛凝视、相机方向、车辆输入和姿态等。 


我们还定义了车辆中三个后视镜的生成和管理逻辑，因为它们默认情况下并未包含在蓝图网格中。将它们分开处理是明智之举，因为在模拟引擎中，使用平面反射实现的后视镜会严重影响性能，因此应谨慎使用。我们还可以为每个后视镜定义画质设置，以动态调整其分辨率及其相应的性能影响。

EgoVehicle 包含指向几乎所有其他主要 DReyeVR 对象的指针，以便它们能够无缝通信。这些指针在构造时设置，并在这些对象的整个生命周期内保持不变。重要的是，EgoVehicle 会生成并附加 EgoSensor，因此它们本质上是相互关联的，彼此不可或缺。

此外，EgoVehicle 的所有输入逻辑都保存在 `EgoInputs.cpp` 源文件中，这样做纯粹是为了将该逻辑与 EgoVehicle 源代码的其余部分分离。

最后，我们在 Carla 世界中生成 EgoVehicle 的方法是：复制一个现有的 Carla 载具蓝图，并将蓝图中的基类 [重新父级化 reparenting](https://forums.unrealengine.com/t/how-to-change-parent-class-of-blueprint-asset/281843) 到我们的 EgoVehicle。该蓝图位于 `EgoVehicle` 的 `内容(Content)` 文件夹中，所有相关的蓝图都整理在这里。


## EgoSensor

- 相关文件： [EgoSensor.h](../DReyeVR/EgoSensor.h), [EgoSensor.cpp](../DReyeVR/EgoSensor.cpp), [DReyeVRSensor.h|cpp](../Carla/Sensor/DReyeVRSensor.h), [DReyeVRData.h|cpp](../Carla/Sensor/DReyeVRData.h)

EgoSensor 是我们用于追踪各种我们可能感兴趣的以人为中心的数据的虚拟 Carla 传感器。它可以被视为一个**在 Carla 世界中运行的隐形数据采集器**。与其他大多数具有物理描述并安装在 Actor 上的 Carla 传感器不同，EgoSensor 会随 EgoVehicle 自动生成和销毁，并在其整个生命周期内绑定到 EgoVehicle 实例。

EgoSensor 是 `DReyeVRSensor` 的子类，而 DReyeVRSensor 又是通用 `CarlaSensor` 的子类，后者源自 Carla 的“["添加传感器教程(add a sensor tutorial)"](https://openhutb.github.io/doc/tuto_D_create_sensor/)”。`DReyeVRSensor` 父类位于代码库的 `CarlaUE4/Plugin/Source` 区域，因为它遵循了 Carla 的规范实现。重要的是，该类是虚类`virtual`（抽象类），这意味着它应该被另一个提供实现的类（即 `EgoSensor`）继承。


由于 DReyeVR 引入了一些 Carla 本身并不依赖的组件（例如用于眼动追踪的 SRanipal 和用于方向盘硬件的 LogitechWheelPlugin），因此我们在 `EgoSensor` 中实现了它们的接口，而不是在 `CarlaUE4/Plugin/Source` 区域（该区域仅供 Carla 使用）。EgoSensor 随后实现了从 SRanipal 和 Logitech 获取数据并将其格式化为适用于当前模拟器时间步的 `DReyeVRData` 数据包所需的方法。


`DReyeVRData` 类是 `CarlaUE4/Plugin/Source/Carla/DReyeVRData.h` 中定义的一系列结构体，它定义了 DReyeVR 跟踪的各种数据类型的结构。例如，它包含了眼睛凝视数据、车辆输入、其他自车变量等结构体。这样的设计旨在鼓励未来的数据类型遵循类似的结构体设计，并与 DReyeVR 进行接口集成，以便将所有数据收集到 `AggregateData` 中，然后作为一个完整的数据包发送到 Python API 进行流式传输，或发送到记录器进行序列化。


EgoSensor 还实现了其他一些不错的功能，例如相机屏幕截图和启用后带有注视点渲染的可变速率着色。

### 继承关系图：

为了阐明这里涉及的继承结构（从老一代到年轻一代）：

1. [`AActor`](https://docs.unrealengine.com/4.27/en-US/API/Runtime/Engine/GameFramework/AActor/) (UE4): 用于在世界中生成任何对象的底层虚幻类
2. [`ASensor`](https://github.com/carla-simulator/carla/blob/0.9.13/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/Sensor.h) (Carla): Carla 参与者为Carla 世界中的传感器表现提供了结构模板
3. [`ADReyeVRSensor`](../Carla/Sensor/DReyeVRSensor.h) (DReyeVR): 该抽象基类 DReyeVRSensor 封装所有和 CARLA 相关的任务逻辑 
    - 流式传输到 PythonAPI
    - 从回放器接收数据以进行重放
    - 包含 `DReyeVR::AggregateData` 实例，其中包含所有数据
4. [`AEgoSensor`](../DReyeVR/EgoSensor.h) (DReyeVR): EgoSensor（派生类）包含全部 DReyeVR 自定义数据成员与业务逻辑。
    - 眼动追踪逻辑（SRanipal）、自车状态采集等。

## DReyeVRPawn

- 相关文件： [DreyeVRPawn.h](../DReyeVR/DReyeVRPawn.h), [DreyeVRPawn.cpp](../DReyeVR/DReyeVRPawn.cpp)


回到我们之前关于玩家与 AI 同时输入 EgoVehicle 的讨论，DReyeVRPawn 是玩家在关卡期间实际控制的实体。与 EgoVehicle/EgoSensor 不同，DReyeVRPawn 不绑定任何特定物体，可以将其视为 **一个定义玩家视口的隐形浮动摄像机** 。

因此，DReyeVRPawn 负责管理游戏内的 [`UCameraComponent`](https://docs.unrealengine.com/4.27/en-US/API/Runtime/Engine/Camera/UCameraComponent/) 组件以及玩家所需的视觉和输入逻辑。[SteamVR](https://docs.unrealengine.com/4.27/en-US/SharingAndReleasing/XRDevelopment/VR/VRPlatforms/SteamVR/QuickStart/) 集成和 LogiWheel 控制方案映射也由它管理，因为这是玩家拥有的对象，因此具有最高的输入优先级。我们还添加了一些视觉效果逻辑，例如用于显示注视轨迹的可视化指示器，该指示器以准星的形式绘制在 [观众屏幕(SpectatorScreen)](https://docs.unrealengine.com/4.26/en-US/SharingAndReleasing/XRDevelopment/VR/DevelopVR/VRSpectatorScreen/) （VR 玩家不可见）或平面屏幕 HUD 上。

EgoVehicle *AI 和玩家* 的双输入逻辑源于 DReyeVRPawn 的实现方式：它只是将指令转发给 EgoVehicle，而不直接控制它，因此 Carla AI 仍然可以控制 EgoVehicle。这使得玩家和 Carla AI 控制器能够同时“控制”EgoVehicle，因为所有玩家的输入仍然会到达 EgoVehicle，并且优先级高于 AI 的输入。

## DReyeVRGameMode

- 相关文件： [DReyeVRGameMode.h](../DReyeVR/DReyeVRGameMode.h), [DReyeVRGameMode.cpp](../DReyeVR/DReyeVRGameMode.cpp)

UE4 中的 [`GameMode`](https://docs.unrealengine.com/4.27/en-US/InteractiveExperiences/HowTo/SettingUpAGameMode/) 用于定义跨关卡的游戏逻辑，这可以通过代码轻松完成（与 [`LevelScripts`](https://docs.unrealengine.com/4.27/en-US/API/Runtime/Engine/Engine/ALevelScriptActor/) 不同，LevelScripts 与单个关卡蓝图绑定）。

游戏模式(gamemode)类很有用，因为 **我们可以依靠它在任何关卡实例中始终存在**，因此我们可以定义超出单个 EgoVehicle/EgoSensor 生命周期的逻辑，并在更全局的层面上进行操作。

例如，我们有代码可以改变游戏内音效的音量，在特定位置生成 EgoVehicle，将控制权转移给默认的浮动观察者（从 EgoVehicle 分离），以及管理记录播放的媒体控制（播放/暂停/单步/倒带等）。

DReyeVR 游戏模式最重要的功能是生成 DReyeVRPawn，这样玩家就可以控制某个角色并与游戏世界进行互动。

## DReyeVRFactory

 - 相关： [DReyeVRFactory.h](../DReyeVR/DReyeVRFactory.h), [DReyeVRFactory.cpp](../DReyeVR/DReyeVRFactory.cpp)

Carla 使用工厂（Factory）来生成所有相关的 Actor（参见 [`CarlaActorFactory`](https://github.com/carla-simulator/carla/blob/master/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Actor/CarlaActorFactory.h)、[`CarlaActorFactoryBlueprint`](https://github.com/carla-simulator/carla/blob/master/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Actor/CarlaActorFactoryBlueprint.h)、[`SensorFactory`](https://github.com/carla-simulator/carla/blob/master/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/SensorFactory.h) 等），这些 Actor 可以生成从车辆、行人到传感器和道具等各种对象。这种设计使得 Carla 能够处理向 LibCarla 注册 Actor 的所有繁琐工作，从而使 LibCarla 能够识别每个 Actor，并允许在 Python 中与它们进行交互。


我们在 `DReyeVRFactory` 中采用了类似的设计，它定义了 DReyeVR 参与者的重要特征，并提供了生成这些参与者所需的逻辑。例如，我们为角色定义了唯一的标签，例如`"harplab.dreyevr_vehicle.model3"`，以避免与现有的 Carla `"vehicle.*"` 查询冲突。


如果您想创建新的 DReyeVR 参与者（例如新的车辆模型）、步行者、传感器等，则需要修改此类。


---

# 向自我传感器(ego-sensor)添加自定义数据

虽然我们的 DReyeVRSensor 提供了一套相当全面的数据，但您可能也有兴趣跟踪我们目前尚未启用的其他数据。

首先要查看的文件是 `Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/`[`DReyeVRData.h`](../Carla/Sensor/DReyeVRData.h) ，其中包含构成自我传感器内容的数据结构。在这里，您需要定义变量及其序列化方法（读/写/打印）。


```c++
/// DReyeVRData.h
class AggregateData // 所有 DReyeVR 传感器数据都保存在这里。
{
public:
    ... // 现有代码
    float GetNewVariable() const;
    ////////////////////:SETTERS://////////////////////

    ...
    void SetNewVariable(const float NewVariableIn);

    ////////////////////:SERIALIZATION://////////////////////
    void Read(std::ifstream &InFile);

    void Write(std::ofstream &OutFile) const;

    FString ToString() const; // 此打印方式用于显示记录器信息

private:
... // existing code
float NewVariable; // <-- 新变量
};
```

然后，您需要将实现代码编写为 `Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/`[`DReyeVRData.cpp`](../Carla/Sensor/DReyeVRData.cpp) 中的内联函数。

```c++
/// DReyeVRData.cpp
...
float AggregateData::GetNewVariable() const
{
    return NewVariable;
}

...
void AggregateData::SetNewVariable(const float NewVariableIn)
{
NewVariable = NewVariableIn;
}

void AggregateData::Read(std::ifstream &InFile)
{
    /// CAUTION: 确保读写操作的顺序相同
    ... // 现有代码
    ReadValue<float>(InFile, NewVariable);
}

void AggregateData::Write(std::ofstream &OutFile) const
{
    /// CAUTION: 确保读写操作的顺序相同
    ... // 现有代码
   WriteValue<float>(OutFile, GetNewVariable());
}

FString AggregateData::ToString() const // 此打印方式用于显示记录器信息
{
    FString print;
    ... // 现有代码
    print += FString::Printf(TEXT("[DReyeVR]NewVariable:%.3f,\n"), GetNewVariable());
    return print;
}
...
```
注意：
- 将相关的变量集合放在结构体中便于更好地组织。为此，我们将 DReyeVRData 设计为包含多个 `DReyeVR::DataSerializer` 对象，每个对象都实现了各自的序列化方法。我们的 `AggregateData` 实例包含了所有结构体以及一个用于访问成员变量的轻量级 API。 
- 以上示例展示了如何直接修改/添加新变量到 `DReyeVR::AggregateData` 对象。但更好的做法是修改现有的 `DReyeVR::DReyeVRSerializer` 对象，或者创建一个新的对象（继承自虚类），并自行定义所有抽象方法。这样可以实现更细粒度的子类/结构体抽象，就像我们大多数变量那样。

完成这一步后，你可以调用 EgoSensor 的 GetData() 获取 EgoSensor 所持有的 DReyeVR::AggregateData 实例，读写新增变量，如下所示：

```c++
// 例如，在其他文件中，例如 EgoVehicle.cpp：
float NewVariable = EgoSensor->GetData()->GetNewVariable();
... // 你的代码
EgoSensor->GetData()->SetNewVariable(NewVariable + 5.f); // 更新新变量
```
  
## [可选] 向 PythonAPI 客户端传输数据：

要从 PythonAPI 客户端查看新数据，您需要将代码复制到 LibCarla 序列化器中。这需要查看  `LibCarla/Sensor/s11n/`[`DReyeVRSerializer.h`](../LibCarla/Sensor/s11n/DReyeVRSerializer.h) 文件，并遵循与其他变量相同的模板：

```c++
class DReyeVRSerializer
{
    public:
    struct Data
    {
        ... // 现有代码
        float NewVariable;

        MSGPACK_DEFINE_ARRAY(
        ... // 现有代码
        NewVariable, // <-- 新变量
        )
    };
};
///注意：您还需要与这个更新后的结构体进行交互：
```
然后，要真正与 DReyeVR 传感器进行交互，您需要修改对 LibCarla 流的调用，以包含您的 `NewVariable`。
```c++
// in Carla/Sensor/DReyeVRSensor.cpp
void ADReyeVRSensor::PostPhysTick(UWorld *W, ELevelTick TickType, float DeltaSeconds)
{
    ... // 现有代码
    Stream.Send(*this,
                carla::sensor::s11n::DReyeVRSerializer::Data{
                    ... // 现有代码
                    Data->GetNewVariable(), // <-- 新变量
                });
} 
```
最后，要实际从 PythonAPI 调用中获取数据，您需要按如下方式修改 DReyeVR 传感器对象的可用属性列表：
```c++
// in LibCarla/source/carla/sensor/data/DReyeVREvent.h
class DReyeVREvent : public SensorData
{
    ...

    public:
    ... // 现有代码
    float GetNewVariable() const // <-- 新代码
    {
        return InternalData.NewVariable;
    }

    private:
    carla::sensor::s11n::DReyeVRSerializer::Data InternalData;
};
```
最后，在这里您将定义要调用哪个函数（变量获取器）来从 PythonAPI 客户端获取数据。
```c++
// in PythonAPI/carla/source/libcarla/SensorData.cpp
class_<csd::DReyeVREvent, bases<cs::SensorData>, boost::noncopyable, boost::shared_ptr<csd::DReyeVREvent>>("DReyeVREvent", no_init)
    ... // 现有代码
    .add_property("new_variable", CALL_RETURNING_COPY(csd::DReyeVREvent, GetNewVariable))
    .def(self_ns::str(self_ns::self))
;
```
修改 `PythonAPI` 或 `LibCarla` 中的文件后，需要重新构建 PythonAPI 才能使更改生效：
```bash
conda activate carla13 # 如果使用 conda
(carla13) make PythonAPI
# 请务必修复可能出现的任何构建错误！
```

# TODO: 添加更多开发笔记

# 技巧与诀窍
## 1. 启用交付模式下的日志记录

在发布模式下查看 CarlaUE4.log 文件非常有用，但这可能是出于性能方面的考虑，Carla（或 Unreal）默认不会这样做？

如果你想启用这些功能，那么你需要在 `Carla/Unreal/CarlaUE4/Source/CarlaUE4.Target.cs` 文件中添加 `bUseLoggingInShipping` 标志。

```cs
public class CarlaUE4Target : TargetRules
{
	public CarlaUE4Target(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		ExtraModuleNames.Add("CarlaUE4");
		bUseLoggingInShipping = true;//  <--- added here
	}
}
```

然后您应该可以在 `C:\Users\%YOUR_USER_NAME%\AppData\Local\CarlaUE4\Saved\Logs\CarlaUE4.log` 找到 CarlaUE4.log 文件（已添加时间戳以避免覆盖）（Windows 系统）。此方法也适用于 Mac/Linux 系统。更多信息请参见 [此处](https://forums.unrealengine.com/t/how-to-debug-shipping-build-exclusive-crash/411138) 。

---

## 2. 如何执行 `LOG`

日志记录对于跟踪代码逻辑和调试非常有用（尤其是在调试 UE4 代码时，调试起来可能比较棘手）。在 Unreal C++ 中，您始终可以使用 `UE_LOG(LogTemp, Log, TEXT("some text and %d here"), 55);`，但我们针对 DReyeVR 的日志记录进行了简化。您可以在编辑 `CarlaUE4/DReyeVR/*.[cpp|h]` 文件时使用我们的 `LOG` 宏（定义在 [`CarlaUE4.h`](../CarlaUE4/CarlaUE4.h) 中）。

主要优势包括：
- 减少程序员（也就是你！）需要编写的样板代码！
- 所有日志都以 `DReyeVRLog` 为前缀，因此可以轻松地在 `CarlaUE4.log` 文件中进行筛选。
- 我们还添加了清晰的编译时前缀，例如`"[{INVOKED_FILE}::{INVOKED_FUNCTION}:{LINE_NUMBER}] {message}"`，以便您可以快速找到此日志的调用位置并将其与其他日志区分开来。 
    - 使用我们宏生成的典型 DReyeVR 日志如下所示：
        ```
        LogDReyeVR: [DReyeVRUtils.h::ReadConfigValue:141] "your message here"
        ```

```c++
... // 在 CarlaUE4/DReyeVR 文件中
void example() {
    LOG("some text and %d (this text is grey)", 55);
    FString warning_str("warning");
    LOG_WARN("some %s here (this text is yellow!)", *warning_str);
    LOG_ERROR("this text is red!");
}
...
```

如果您使用的是 `CarlaUE4/Plugins/Source/Carla` 代码库，则可以使用类似的宏，但要加上 `DReyeVR_` 前缀：`DReyeVR_`: `DReyeVR_LOG("blah blah")`、`DReyeVR_LOG_WARN("blah blah warning")` 等。

---

## 3. 管理多个 Carla/DReyeVR 版本
- 使用独立的 `python` 环境（例如 `conda`）对于在同一台机器上运行不同版本的 Carla Python 包（例如 `LibCarla`）非常有用。为此，您可以按照 [`Install.md`](Install.md) 中的说明，为每个 Carla 版本创建一个单独的 conda 环境。请记住，需要针对每个 shell 激活新的 `conda` 环境！
- 如果您计划安装多个 CARLA 版本，则需要使用相应的 `Content` 更新它们。与其每次都调用`Update`脚本来更新，不如保存 `Content.tar.gz` 文件，并在每次创建新仓库时将其复制到新的 `Unreal/CarlaUE4/Content/Carla` 目录中。

---

## 4. TODO 添加更多技巧和诀窍
