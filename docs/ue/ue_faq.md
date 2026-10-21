# 虚幻引擎

- [__文档__](#documentation)
    - [理解基础概念](#baisc_concept)
- [__操作__](#op)
- [__蓝图__](#blueprint)
- [__编程__](#program)
- [__杂项__](#misc)
- [__源代码分析__](#src_analysis)
- [__其他__](#other)
- [__加速__](#speed_up)
- [__插件__](#plugin)
- [__源代码管理__](#src_management)
- [__常见问题__](#faq)
- [__参考链接__](#ref_link)



## 文档 <span id="documentation"></span>

### 理解基础概念 <span id="baisc_concept"></span>

#### 关卡
[更改默认关卡](https://openhutb.github.io/engine_doc/zh-CN/Basics/Levels/HowTo/ChangeDefaultLevel/index.html)


### 操作 <span id="op"></span>

* [命令行+快捷键](./command.md)


## 蓝图 <span id="blueprint"></span>
* [蓝图快速入门指南](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/blueprints-quick-start-guide?application_version=4.27)
* [持有棋子](https://dev.epicgames.com/documentation/en-us/unreal-engine/possessing-pawns?application_version=4.27)

## 编程  <span id="program"></span>
[`class ENGINE_API`](https://github.com/CarlaUnreal/UnrealEngine/pull/38/files) 是一个宏，用于控制类的导出行为，确保类在不同模块（DLL或共享库）之间正确使用。

## 杂项 <span id="misc"></span>
* [语法](syntax.md)
* [像素流推送](./pixel_streaming.md)
* [配置说明](./config.md)
* [虚幻引擎commandlet](ue_commandlet.md)
* [虚幻引擎管线](ue_pipeline.md)
* [虚幻引擎相关效果](effect.md)
* [着色器](shader.md)
* [虚幻编辑器](unreal_editor.md)


## 源代码分析  <span id="src_analysis"></span>

* [USkeletalMeshComponent](https://zhuanlan.zhihu.com/p/637746453)
* [Actor生命周期](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/actor-lifecycle?application_version=4.27)

### UAT.bat参数分析

构建发布版的命令：`Engine\Build\BatchFiles\RunUAT.bat BuildGraph -target="Make Installed Build Win64" -script=Engine/Build/InstalledEngineBuild.xml -clean -set:HostPlatformOnly=true -set:WithDDC=false`

搜索`Engine/Build/InstalledEngineBuild.xml`配置文件中的`Node Name=`，可以替换中间的`-target`来进行切换：

* `Compile UE4Editor Win64` 构建编辑器
* `Compile UE4Game Win64`




## 其他 <span id="misc"></span>

* [Windows 下的可发布包的构建](../launch_windows.md)

* 源代码版引擎的缓存路径位于项目的DeriveDataCache目录下：`hutb\Unreal\CarlaUE4\DerivedDataCache`（定义在`engine\Engine\Config\BaseEngine.ini`的`[InstalledDerivedDataBackendGraph]`变量组中）
```shell
Boot=(Type=Boot, Filename="%ENGINEUSERDIR%DerivedDataCache/Boot.ddc", MaxCacheSize=512)
```

* [PIE 和 SIE](https://blog.csdn.net/qq_43497224/article/details/129336509)

默认运行测试位置：菜单栏中央，三角形按钮。或者按

Play Modes
运行（测试）模式主要有两种，编辑器中运行（PIE, Play In Editor）或在编辑器中模拟（SIE, Simulate In Editor）。

**编辑器中运行**的意思是：Play，玩。你做的游戏是如何让玩家操控游玩的，在这里就是如何操控游玩的。（比如第一人称游戏，PIE下就是鼠标控制摄像机视角旋转，方向键移动,）

**编辑器中模拟**的意思是：模拟，测试。在这个模式下相当于是上帝视角。此时游戏在运行，但是我们仍然可以用之前做游戏（摆放地图关卡Actor、修改运行时参数）的方式修改这个世界。


PIE和SIE切换：
在PIE模式下，shift + F1可以获得鼠标控制权（一般第一人称第三人称下鼠标用于旋转方向摄像头，不会出现光标）。然后点击工具栏的弹出（Eject）可以切换到SIE

你也可以点击 控制（Possess） 功能的快捷键（F8）来从在编辑器中模拟（SIE）切换到在编辑器中运行（PIE）。


## 加速构建过程  <span id="speed_up"></span>

每次执行hutb的make的操作时，都会出现
```text
Using 'git status' to determine working set for adaptive non-unity build (D:\work\workspace\UnrealEngine).
Waiting for 'git status' command to complete
Target is up to date
Total execution time: 2.38 seconds
```
可以 [移除虚幻引擎的`.git`目录](https://github.com/adamrehn/ue4-docker/commit/9cf1375c33098a2787b5f514fd0ff36167a12b96) 来禁用 UBT 的 `git status` 调用，达到加速构建流程的作用。

此功能用于从 Unity 构建中排除大多数迭代文件。这应该会降低编译速度（如果你经常构建引擎，这个功能确实很有用，但大多数情况下并非如此）。

要禁用此行为，您可以更改 `Engine\Saved\UnrealBuildTool\BuildConfiguration.xml` 里的`<Configuration> </Configuration>`中添加：
```text
  <SourceFileWorkingSet>
	<Provider>None</Provider>
  </SourceFileWorkingSet>
```


## 插件 <span id="plugin"></span>
### USD
Universal Scene Description (USD) 是通用场景描述，一个开放且可扩展的生态系统，用于在 3D 世界中描述、组合、模拟和协作，最初由皮克斯动画工作室发明；是 Omniverse 使用的文件格式，人称元宇宙的 HTML。


什么是仿真就绪（SimReady）素材


仿真就绪（SimReady）素材是虚拟世界的基础模块，SimReady 素材不仅仅是 3D 物件，它们包含基于 Universal Scene Description (USD) 构建的准确物理属性、行为和连接的数据流。


## 编译  <span id="compilation"></span>


###### make launch启动引擎编辑器时报错
报错信息：
```text
无法启动D:/hutb/Build/engine/Engine/Binaries/Win64/ShaderCompileWorker.exe
需要编译ShaderCompileWorker。
```
原因：`D:\hutb\Build\engine\Engine\Binaries\Win64`目录下没有编译出`ShaderCompileWorker.exe`。

因为没有VS2019，导致Build.bat中执行`call "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\MSBuild\Current\bin\MSBuild.exe" UE4.sln  /p:Configuration="Development Editor" /p:Platform="Win64" /p:Project="UnrealBuildTool" /p:OutputPath=.\`没有成功


###### 编译UE时报错：使用“override”声明的成员函数不能重写基类成员
出错位置：`D:\work\workspace\UnrealEngine\Engine\Source\Runtime\CoreUObject\Public\UObject\CoreNet.h` 345 行
```C++
	virtual FArchive& operator<<(FSoftObjectPath& Value) override;
```


###### 编译AirSim后，启动编译器崩溃
报错信息：
```text
Assertion failed: ResourceTableFrameCounter == INDEX_NONE [File:D:/work/workspace/UnrealEngine/Engine/Source/Runtime/Windows/D3D11RHI/Private/D3D11Texture.cpp] [Line: 2260]

UE4Editor_Core!AssertFailedImplV() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Core\Private\Misc\AssertionMacros.cpp:104]
UE4Editor_Core!FDebug::CheckVerifyFailedImpl() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Core\Private\Misc\AssertionMacros.cpp:461]
UE4Editor_D3D11RHI!FD3D11DynamicRHI::RHIUpdateTextureReference() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Windows\D3D11RHI\Private\D3D11Texture.cpp:2260]
UE4Editor_RHI!FRHICommandListImmediate::UpdateTextureReference() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\RHI\Private\RHICommandList.cpp:2730]
UE4Editor_Engine!FStreamableTextureResource::FinalizeStreaming() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Engine\Private\Rendering\StreamableTextureResource.cpp:220]
UE4Editor_Engine!FTexture2DUpdate::DoFinishUpdate() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Engine\Private\Streaming\Texture2DUpdate.cpp:158]
UE4Editor_Engine!FTexture2DStreamIn_DDC_AsyncCreate::Finalize() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Engine\Private\Streaming\Texture2DStreamIn_DDC_AsyncCreate.cpp:84]
UE4Editor_Engine!TRenderAssetUpdate<FTexture2DUpdateContext>::TickInternal() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Engine\Private\Streaming\RenderAssetUpdate.inl:76]
UE4Editor_Engine!<lambda_c13beac94fedf293002b1e0b20710a81>::operator()() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Engine\Private\Streaming\RenderAssetUpdate.cpp:270]
UE4Editor_Engine!TEnqueueUniqueRenderCommandType<`FRenderAssetUpdate::ScheduleRenderTask'::`2'::RenderAssetUpdateCommandName,<lambda_c13beac94fedf293002b1e0b20710a81> >::DoTask() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\RenderCore\Public\RenderingThread.h:183]
UE4Editor_Engine!TGraphTask<TEnqueueUniqueRenderCommandType<`FRenderAssetUpdate::ScheduleRenderTask'::`2'::RenderAssetUpdateCommandName,<lambda_c13beac94fedf293002b1e0b20710a81> > >::ExecuteTask() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Core\Public\Async\TaskGraphInterfaces.h:886]
UE4Editor_Core!FNamedTaskThread::ProcessTasksNamedThread() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Core\Private\Async\TaskGraph.cpp:709]
UE4Editor_Core!FNamedTaskThread::ProcessTasksUntilQuit() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Core\Private\Async\TaskGraph.cpp:601]
UE4Editor_RenderCore!RenderingThreadMain() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\RenderCore\Private\RenderingThread.cpp:373]
UE4Editor_RenderCore!FRenderingThread::Run() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\RenderCore\Private\RenderingThread.cpp:509]
UE4Editor_Core!FRunnableThreadWin::Run() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Core\Private\Windows\WindowsRunnableThread.cpp:86]
```

> [原因](https://github.com/carla-simulator/carla/issues/6201#issuecomment-1436199677) ：把Ue4NoEditor的附加地图包和从源码编译的ue4editor搞混了，所以把附加地图的引擎文件夹文件放到了unreal4.26.2的文件夹里。
> 
> 未使用的 [暂时解决办法](https://github.com/carla-simulator/carla/issues/6075#issuecomment-1623373687) ：直接注释掉 D3D11Texture.cpp 中引发错误的那行代码 (l. 2260) 。 或者 [改配置文件](https://forums.unrealengine.com/t/ue-4-26-built-from-source-crashes-when-opening-project/739873/10)


Carla 编辑器运行崩溃：
```text
LoginId:bc22576a452b36c1831fe8942b55e57a
EpicAccountId:77cf3795af004e58a037e9c9d4a5aa0d

Unhandled Exception: EXCEPTION_STACK_OVERFLOW

user32
user32
sdk_legacy_steering_wheel_x64
user32
user32
sdk_legacy_steering_wheel_x64
```


###### 使用vs2022编译UE4.26时候报错
```text
LIN110 无法打开文件“D:\work\workspace\UnrealEngine\Engine\Binaries\Win64\UE4Editor-Engine.dll”
LIN110 无法打开文件“D:\work\workspace\UnrealEngine\Engine\Binaries\Win64\UE4Editor-UnrealEd.dll”
LIN110 无法打开文件“D:\work\workspace\UnrealEngine\Engine\Binaries\Win64\UE4Editor-Chaos.dll”
LIN110 无法打开文件“D:\work\workspace\UnrealEngine\Engine\Binaries\Win64\UE4Editor-DetailCustomization.dll”
```
在对应目录中存在。

[解决](https://forums.unrealengine.com/t/link-fatal-error-lnk1104-cannot-open-file/287530/11) ：使用`资源监视器`找到`UEEditor.exe`对应的进程，结束进程，然后就可以启动虚幻编辑器了（原因不明）。


###### 编译警告：Detected compiler newer than Visual Studio 2019, please update min version checking in WindowsPlatformCompilerSetup.h




##### 如何修改编译使用的CPU核心数量

修改Engine\Saved\UnrealBuildTool\BuildConfiguration.xml文件中的配置：
```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ProjectFileGenerator>
        <Format>VisualStudio2019</Format>
    </ProjectFileGenerator>
    <ParallelExecutor>
        <ProcessorCountMultiplier>0.75</ProcessorCountMultiplier>
        <MaxProcessorCount>24</MaxProcessorCount>
    </ParallelExecutor>
</Configuration>
```

否则还可能 [报错](https://ue5wiki.com/wiki/5cc4f8a/) ：
```text
  c1xx: fatal error C1076: 编译器限制: 达到内部堆限制
  [3/37] DReyeVRGameMode.gen.cpp
  c1xx: error C3859: 未能创建 PCH 的虚拟内存
  c1xx: note: 系统返回代码 1455: The paging file is too small for this operation to complete.
```

###### 打包时候报错：
```text
Package ../../../../../Unreal/CarlaUE4/Content/Carla/Content/Matrials/HutbCity/BeiMen/Default_Material.uasset has malformed tag
```
检查是否没有拉取大文件。

## 源代码管理  <span id="src_management"></span>

###### [从原来的仓库迁移到OpenHUTB的引擎仓库](https://www.cnblogs.com/gjmhome/p/14061090.html)
1.修改文件`.git/config`远端的仓库地址
```shell
[remote "origin"]
	url = https://github.com/OpenHUTB/engine.git
	fetch = +refs/heads/*:refs/remotes/origin/*
```

2.合并两个不相关的仓库：
```shell
git pull -f origin hutb --allow-unrelated-histories
```

3.丢弃本地提交，强制回到线上最新版本：
```shell
git reset --hard origin/hutb
```


## 常见问题  <span id="faq"></span>

###### CarlaUE4.exe 崩溃的日志保存目录

.dmp 文件分析要求本机中有崩溃发生版本对应的符号表文件（CarlaUE4.pdb 文件），使用 VS 2022 （VS 2019 的步骤类似）分析 .dmp 文件步骤如下：

```shell
# CarlaUE4.exe崩溃后的日志目录
C:\Users\Administrator\AppData\Local\CarlaUE4\Saved\Crashes
# 启动引擎编辑器时崩溃的日志目录
hutb\Unreal\CarlaUE4\Saved\Crashes\UE4CC-Windows-{ID}\CarlaUE4.log
```
附：崩溃日志的保存目录和项目名有关：`C:\Users\{Your Windows Username}\AppData\Local{Project Name}\Saved\Crashes\`

###### 引擎 MiniDump 崩溃现场的恢复

1.找到崩溃时生成的 .dmp 文件，使用 VS 2022 打开，如下图所示：
![](../img/tuto_D_windows_debug/open_dump.jpg)

（打开文件后会有转储摘要、系统信息、引用模块的说明，但这些信息并不直观）。

点击设置符号路径。该按钮在界面右侧，用于指定 CarlaUE4.pdb 文件的路径。


2.选择 .pdb 文件的路径，路径为编译好的 HUTB 源码的 `D:\hutb\Unreal\CarlaUE4\Binaries\Win64` 路径下，点击确定

![](../img/tuto_D_windows_debug/select_pdb.jpg)

3.点击 "使用 仅限本机 进行调试"，成功复现崩溃现场

![](../img/tuto_D_windows_debug/restore_scene.jpg)

然后就可以在VS右下角的`调用堆栈`中查看堆栈中代码报错的行。

###### 编辑器中运行(PIE)场景时添加命令行参数

在自动测试时，需要在`CarlaUE4.exe`后面添加一些参数，操作步骤如下：

1.在编辑器的菜单中：编辑(Edit) -> 编辑器偏好设置(Editor Preferences) -> 播放(Play) -> 在独立进程游戏中运行(Play in Standalone game)，有一个文本框`附加启动参数`，可以在这里添加启动所需的参数（比如：`--carla-rpc-port=3654 --carla-streaming-port=0 -nosound`）

2.点`运行`中的三角下拉菜单中的`独立进程游戏`启动场景（直接点运行附带的参数不生效）

###### 有风时叶子闪烁

编辑`Content/Carla/Static/Vegetation/Trees/Materials/FanPalm/MexicanFanPalm_Main_Leaf`（对所有树都有效），并进入`MF_SimpleGrassWind`，将`VisualTime`和`Input WindSpeed (Scalar)`后的第二个 `Multiply`中B的输入由`-0.5`改为`-1`（使其可抖动的范围更大，避免闪烁）。


## 参考链接 <span id="ref_link"></span>
* [**UE 4 C++ 教程**](https://bbs.huaweicloud.com/blogs/310592)

* [UE4初学者系列教程合集-全中文新手入门教程](https://www.bilibili.com/video/BV164411Y732/?share_source=copy_web&vd_source=d956d8d73965ffb619958f94872d7c57)

* [ue4官方文档](https://docs.unrealengine.com/4.26/zh-CN/)

* [官方讨论社区](https://forums.unrealengine.com/categories?tag=unreal-engine)

* [知乎的虚幻引擎社区](https://zhuanlan.zhihu.com/egc-community)

* [虚幻引擎开放路线图](https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/tabs/24-unreal-engine-4-27)

* [UE4中的C++编程简介](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/introduction-to-cplusplus-programming-in-ue4?application_version=4.27)

* [Unreal 的 MiniDump 机制调研](https://zhuanlan.zhihu.com/p/649610542)

