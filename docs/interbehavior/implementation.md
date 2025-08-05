# 虚拟现实的实现

配置文件 `Unreal/CarlaUE4/Config/DReyeVRConfig.ini` 中的 `CameraPose`配置了相机的初始位置。


## 配置
默认的引擎配置在`carla\Unreal\CarlaUE4\Config\DefaultEngine.ini`文件中进行修改：
```shell
# 传统模式
# GlobalDefaultServerGameMode=/Game/Carla/Blueprints/Game/CarlaGameMode.CarlaGameMode_C
# 默认的游戏模式（VR模式，区别于传统模式），运行的脚本位于：carla\Unreal\CarlaUE4\Source\CarlaUE4\DReyeVR\DReyeVRGameMode.cpp
GlobalDefaultGameMode=/Script/CarlaUE4.DReyeVRGameMode
GlobalDefaultServerGameMode=/Script/CarlaUE4.DReyeVRGameMode
```

## 分析
玩家控制器（PlayerController）负责指挥棋子（Pawn），而 Pawn 的占有需要指定 PlayerController。





## 在最新的版本上编译
解决问题的过程：

InputComponent != nullptr是空

解决：`Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/DReyeVRPawn.cpp`


```shell
void ADReyeVRPawn::BeginEgoVehicle(AEgoVehicle *Vehicle, UWorld *World)
{
    /// NOTE: this should be run very early!
    // before anything that needs the EgoVehicle pointer (since this initializes it!)

    SetEgoVehicle(Vehicle);
    ensure(EgoVehicle != nullptr);
    EgoVehicle->SetPawn(this);

    if (GetPlayer() == nullptr)
        return;
    InputComponent = NewObject<UInputComponent>(this);
    InputComponent->RegisterComponent();

    // register inputs that require EgoVehicle
    // ensure(InputComponent != nullptr);
    if (IsValid(InputComponent))
    {
        SetupEgoVehicleInputComponent(InputComponent, EgoVehicle);
    }
}
```


崩溃是因为 InputComponent 是 `nullptr`。如果没有 PlayerController 拥有 pawn，就会发生这种情况。您需要做的就是将使用输入组件的行换行if (IsValid(InputComponent)) { ... }。

DReyeVRGame->GetPawn() 为空

已经有车辆生成，而且有声音，但是没有持有棋子（车辆），即 `InputComponent != nullptr` 不成立。 

调用流程：
D:\work\workspace\carla\Unreal\CarlaUE4\Source\CarlaUE4\DReyeVR\DReyeVRGameMode.cpp

`ADReyeVRGameMode::SetupEgoVehicle()`

`SpawnEgoVehicle(SpawnPt);`

`void ADReyeVRGameMode::SpawnEgoVehicle(const FTransform &SpawnPt)`

`EgoVehiclePtr = static_cast<AEgoVehicle *>(Episode->SpawnActor(SpawnPt, DReyeVRDescr));`

Get Input Component 返回当前的 InputComponent，这会返回 NULL（除非bReceivesEditorInput设置为true）

有一个自定义 Pawn，当在 GameMode 中将其设置为默认值时，它会自动生成，并且键绑定可以正常工作（即“InputComponent”不为 NULL），但是当我从关卡蓝图或游戏管理器蓝图生成实例时，[“InputComponent”为 NULL](https://forums.unrealengine.com/t/why-inputcomponent-is-null-when-spawn-from-bp/581079) 。

必须在 BP 中启用自动占有并选择 Player 0。我猜这启用了 InputComponent！


D:\work\workspace\carla\Unreal\CarlaUE4\Source\CarlaUE4\DReyeVR\EgoVehicle.cpp

`SetGame(Cast<ADReyeVRGameMode>(UGameplayStatics::GetGameMode(World)));`

`DReyeVRGame->GetPawn()->BeginEgoVehicle(this, World);`

D:\work\workspace\carla\Unreal\CarlaUE4\Source\CarlaUE4\DReyeVR\DReyeVRPawn.cpp
`ensure(InputComponent != nullptr);`

---
carla\Unreal\CarlaUE4\Plugins\Carla\Source\Carla\Vehicle\CarlaWheeledVehicle.cpp 和 CarlaWheeledVehicle.h 前后差别很大

交通管理器生成的车不跑

---



原来适配的虚幻引擎的提交记录只到 [Commit d40ec35](https://github.com/OpenHUTB/UnrealEngine/commit/d40ec35474e8793b4eea60dba6c4f051186e458e) 。

1.运行`DReyeVR/Scripts/install.py`将必要的代码复制到carla目录中；

2.调整代码，比较复杂的是：Unreal/CarlaUE4/Config/DefaultEngine.ini

原始仓库拷贝到目的目录存在`Scripts/Paths/DReyeVR.csv`中，


carla\Unreal\CarlaUE4\Source\CarlaUE4\DReyeVR/FlatHUD.h 的结构体HUDLine 和 carla/rpc/DebugShape.h 中的 HUDLine 重命，将其改为 VRLine

为什么不能在头文件定义static变量
可以通过编译，但是使用static定义变量证明该变量的作用域范围仅在该源文件内，其他源文件不能访问。如果在头文件中定义static变量，证明包含了所有这个头文件的源文件都定义了该变量，会造成变量多次定义浪费内存，而且不是真正的全局变量。

参考[链接](https://blog.csdn.net/qq_28258885/article/details/115769975) 解决静态方法在其他文件中找不到的问题。
Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/V2X/CaService.cpp 导入.cpp文件

carla\LibCarla\source\carla\streaming\detail\tcp/ServerSession.h中的
```cpp
template <typename... Buffers>
static auto MakeMessage(Buffers... buffers) {
  static_assert(
      are_same<BufferView, Buffers...>::value,
      "This function only accepts arguments of type BufferView.");
  return std::make_shared<const Message>(buffers...);
}
```
SharedBufferView改为 BufferView。不然报错：只接受BufferView类型。


注释掉 `carla\Unreal\CarlaUE4\Source\CarlaUE4\DReyeVR` 中的：
```cpp
Replayer->Restart();
Replayer->Advance(1.0);
Replayer->Advance(-1.0);
```
否则出现错误：
```text
DReyeVRGameMode.cpp.obj : error LNK2019: 无法解析的外部符号 "public: void __cdecl CarlaReplayer::Restart(void)"
```


执行生成交通报错：
```text
Assertion failed!
Program:...4\Plugins\Carla\BinarieslWin64\UE4Editor-Carla.dllFile: D:\workworkspacelcarlalLibCarlalso...ServerS..ion.cppLine: 106
Expression: (bytes)==(sizeof(message_size_type) +message->size())
```
即`carla\LibCarla\source\carla\streaming\detail\tcp\ServerSession.cpp`中的这一行报错：
```cpp
DEBUG_ASSERT_EQ(bytes, sizeof(message_size_type) + message->size());
```


## 各个模块



### 头显模块

