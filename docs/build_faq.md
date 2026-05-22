# 常问的问题

此处列出了有关 Carla 安装和构建的一些最常见问题。更多信息可以在该项目的 [GitHub issues](https://github.com/carla-simulator/carla/issues?utf8=%E2%9C%93&q=label%3Aquestion+) 找到。如果您没有发现此处列出的疑问，请查看论坛并随时提问。

<div class="build-buttons">
<p>
<a href="https://github.com/OpenHUTB/hutb/discussions" target="_blank" class="btn btn-neutral" title="跳转至 HUTB 论坛">
HUTB 论坛</a>
</p>
</div>

---

## 专业问题

* [传感器](./faq/sensor.md)
* [动力学](./faq/dynamics.md)


## 系统要求

* [构建 Carla 所需的磁盘空间。](#expected-disk-space-to-build-carla)
* [运行 Carla 的推荐硬件。](#recommended-hardware-to-run-carla)

---

## Linux 构建

* [从 GitHub 下载时不会出现“CarlaUE4.sh”脚本。](#carlaue4sh-script-does-not-appear-when-downloading-from-github)
* [“make launch” 在 Linux 上不起作用。](#make-launch-is-not-working-on-linux)
* [克隆虚幻引擎存储库显示错误。](#cloning-the-unreal-engine-repository-shows-an-error)
* [AttributeError: module 'carla' has no attribute 'Client' when running a script.](#attributeerror-module-carla-has-no-attribute-client-when-running-a-script)
* [无法运行示例脚本或 "RuntimeError: rpc::rpc_error during call in function version".](#cannot-run-example-scripts-or-runtimeerror-rpcrpc_error-during-call-in-function-version)

---

## Windows 构建

* [从 GitHub 下载时不会出现“CarlaUE4.exe”。](#carlaue4exe-does-not-appear-when-downloading-from-github)
* [CarlaUE4 无法编译。尝试从源手动重建它。](#carlaue4-could-not-be-compiled-try-rebuilding-it-from-source-manually)
* [即使 CMake 已正确安装，也会显示 CMake 错误。](#cmake-error-shows-even-though-cmake-is-properly-installed)
* [Error C2440, C2672：编译器版本。](#error-c2440-c2672-compiler-version)
* [“make launch”在 Windows 上不起作用。](#make-launch-is-not-working-on-windows)
* [Make 缺少 libintl3.dll 或/和 libiconv2.dll。](#make-is-missing-libintl3dll-orand-libiconv2dll)
* [模块缺失或使用不同的引擎版本构建。](#modules-are-missing-or-built-with-a-different-engine-version)
* [在 `PythonAPI/carla` 中尽管成功输出消息，但没有`dist`文件夹](#there-is-no-dist-folder-in-pythonapicarla-despite-a-successful-output-message)
* [osm2odr-visualstudio为空，或者拷贝过去的目录不对](#osm2odr_is_null)
* [类型转换不对](#type_conversion_error)
* [链接不到osm2odr.lib](#link_osm2odr_failed)
* [编译器的堆空间不足](#heap_lack)


---

## 编译 OpenHUTB 分支



### make lanunch ARGS="--chrono"报错
```text
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(219): error C2653: “CubemapHelpersFisheye”: 不是类或命名空间名称
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(279): note: 查看对正在编译的函数 模板 实例化“void AFisheyeSensor::SendPixelsInRenderThread<AFisheyeSensor>(TSensor &,float,float,float,float,float,float,float,float,float,float,float)”的引用
      with
      [
          TSensor=AFisheyeSensor
      ]
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(219): error C2065: “FFisheyeParams”: 未声明的标识符
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(219): error C2146: 语法错误: 缺少“;”(在标识符“FisheyeParams”的前面)
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(219): error C2065: “FisheyeParams”: 未声明的标识符
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(221): error C2065: “FisheyeParams”: 未声明的标识符
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(223): error C2065: “FisheyeParams”: 未声明的标识符
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(225): error C2065: “FisheyeParams”: 未声明的标识符
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(227): error C2065: “FisheyeParams”: 未声明的标识符
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(229): error C2653: “CubemapHelpersFisheye”: 不是类或命名空间名称
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(229): error C2065: “FisheyeParams”: 未声明的标识符
D:/work/workspace/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/FisheyeSensor.cpp(229): error C3861: “GenerateLongLatUnwrapFisheye”: 找不到标识符
```
> 因为鱼眼相机需要修改虚幻引擎中的代码，需要同步更新 [引擎仓库](https://github.com/OpenHUTB/engine) hutb 分支中的代码。

---

## 运行 Carla

* [运行Carla_0.9.12.sh时候报错：error while loading shared libraries: libomp.so.5](#load_libraries)
* [在虚幻编辑器中运行服务器时 FPS 速率较低。](#low-fps-rate-when-running-the-server-in-unreal-editor)
* [无法运行脚本。](#cant-run-a-script)
* [当在虚幻编辑器中运行时链接到模拟器。](#connect-to-the-simulator-while-running-within-unreal-editor)
* [无法运行 Carla，无论是二进制还是源代码构建。](#cant-run-carla-neither-binary-nor-source-build)
* [ImportError: DLL load failed: The specified module could not be found.](#importerror-dll-load-failed-the-specified-module-could-not-be-found)
* [ImportError: DLL load failed while importing libcarla: %1 is not a valid Win32 app.](#importerror-dll-load-failed-while-importing-libcarla-1-is-not-a-valid-win32-app)
* [ImportError: No module named 'carla'](#importerror-no-module-named-carla)
* [RuntimeError: rpc::rpc_error during call in function apply_batch](#rpc_error)
* [ValueError: sticky_control: invalid value type](#value_error)
---

## 其他

* [Fatal error: 'version.h' has been modified since the precompiled header.](#fatal-error-versionh-has-been-modified-since-the-precompiled-header)
* [创建 Carla 的二进制版本。](#create-a-binary-version-of-carla)
* [我可以在 Linux 计算机上打包适用于 Windows 的 Carla，反之亦然吗？](#can-i-package-carla-for-windows-on-a-linux-machine-and-vice-versa)
* [如何卸载 Carla 客户端库？](#how-do-i-uninstall-the-carla-client-library)

---

<!-- ======================================================================= -->
## 系统要求
<!-- ======================================================================= -->

###### 构建 Carla 所需的磁盘空间。 <span id="expected-disk-space-to-build-carla"></span>

> 建议至少有 170GB 可用空间。构建 Carla 需要大约 35GB 的磁盘空间，加上虚幻引擎大约需要 95-135GB。

<!-- ======================================================================= -->

###### 运行 Carla 的推荐硬件。 <span id="recommended-hardware-to-run-carla"></span>

> Carla 是一款性能要求较高的软件。它至少需要 6GB GPU，或者更好的是能够运行虚幻引擎的专用 GPU。
>
> 看看 [虚幻引擎推荐的硬件](https://www.ue4community.wiki/recommended-hardware-x1p9qyg0) 。

---

## Linux 构建
<!-- ======================================================================= -->
###### 从 GitHub 下载时不会出现“CarlaUE4.sh”脚本。 <span id="carlaue4sh-script-does-not-appear-when-downloading-from-github"></span>

> Carla 的源版本中没有 `CarlaUE4.sh` 脚本。按照 [构建说明](build_linux.md) 从源代码构建 Carla。
> 
> 要使用 `CarlaUE4.sh` 运行 Carla，请按照 [快速启动安装](start_quickstart.md) 进行操作。

<!-- ======================================================================= -->

###### “make launch”在 Linux 上不起作用。 <span id="make-launch-is-not-working-on-linux"></span>

> 在构建安装过程中可能会拖出许多不同的问题，并会像这样显现出来。以下是最可能的原因列表：
> 
> * __运行虚幻引擎 4.26。__ 构建虚幻引擎时可能出现某些问题。尝试单独运行虚幻编辑器并检查它是否是 4.26 版本。
> * __下载资产。__ 如果没有视觉内容，服务器将无法运行。此步骤是强制性的。
> * __UE4_ROOT 未定义。__ 境变量未设置。请记住通过将其添加到 `~/.bashrc` 或 `~/.profile` 来使其在会话范围内持久存在。否则，需要为每个新 shell 进行设置。运行`export UE4_ROOT=<path_to_unreal_4-26>`设置这次的变量。
> * __检查依赖。__ 确保一切都安装正确。也许其中一个命令被跳过、不成功或者依赖项不适合系统。
> * __Numpy 2 冲突__. NumPy 2 与用于构建 CARLA 的工具存在冲突。这是导致 Boost 相关错误的最常见原因之一。请使用 `python3 -m pip show numpy` 命令检查您的 NumPy 版本。如果版本为 2.0.0 或更高，则必须降级到 *numpy<2.0.0* 的版本。
> * __删除 Carla 并再次克隆它。__ 以防万一出了问题。删除 Carla 并重新克隆或下载。
> * __满足系统要求。__ Ubuntu 版本应为 16.04 或更高版本。Carla 需要大约 170GB 的磁盘空间和一个专用 GPU（或至少一个 6GB）才能运行。
> 
> 系统显示与 Carla 冲突的其他特定原因可能会发生。请将这些内容发布到 [论坛](https://github.com/OpenHUTB/hutb/discussions) 上，以便团队可以更多地了解它们。 

<!-- ======================================================================= -->

###### 克隆虚幻引擎存储库显示错误。 <span id="cloning-the-unreal-engine-repository-shows-an-error"></span>

> __1. 虚幻引擎帐号是否已激活？__ 虚幻引擎存储库是私有的。为了克隆它，请创建虚 [幻引擎帐](https://www.unrealengine.com/en-US/) 户，激活它（检查验证邮件），然后 [链接您的 GitHub](https://www.unrealengine.com/en-US/blog/updated-authentication-process-for-connecting-epic-github-accounts)  帐户。
> 
> __2. git是否安装正确？__ 有时错误表明与 `https` 协议不兼容。通过卸载并重新安装 git 即可轻松解决。打开终端并运行以下命令：
>
>      sudo apt-get remove git # 卸载 git
>      sudo apt install git-all # 安装 git
> 

<!-- ======================================================================= -->

###### AttributeError: module 'carla' has no attribute 'Client' when running a script. <span id="attributeerror-module-carla-has-no-attribute-client-when-running-a-script"></span>

> 运行以下命令。
> 
> 
>       pip3 install -Iv setuptools==47.3.1
>  
>
> 并再次构建 PythonAPI。
> 
>
>      make PythonAPI
>
>
> 尝试构建文档来测试一切是否正常运行。应该会显示成功的消息。
>
>      make PythonAPI.docs

<!-- ======================================================================= -->

###### 无法运行示例脚本或 "RuntimeError: rpc::rpc_error during call in function version". <span id="cannot-run-example-scripts-or-runtimeerror-rpcrpc_error-during-call-in-function-version"></span>

> ![faq_rpc_error](img/faq_rpc_error.jpg)
>
> 如果运行脚本返回与此类似的输出，则说明 PythonAPI 中的 `.egg` 文件存在问题。

!!! 重要
    如果您使用的是 0.9.12+，有多种方法可以使用/安装客户端库。如果您使用客户端库（`.whl` 或 PyPi 下载）的较新方法之一，本节中的信息将与您无关。
> 
> 首先，打开`<root_carla>/PythonAPI/carla/dist`。 应该有一个和你正在使用相对应的 Carla 和 Python 响应的 `.egg` 文件（类似于 `carla-0.X.X-pyX.X-linux-x86_64.egg`）。确保该文件与您正在使用的 Python 版本匹配。要检查您的 Python 版本，请使用以下命令。 
> 
> 
>       python3 --version
>       # 或者对于 Python 2
>       python --version
> 
>
> 如果文件丢失或者您认为它可能已损坏，请尝试再次重建。
>
>      make clean
>      make PythonAPI
>      make launch
>
>  
> 现在再次尝试示例脚本之一。 
>
>      cd PythonAPI/examples
>      python3 dynamic_weather.py
>
> 如果错误仍然存在，则问题可能与您的 PythonPATH 有关。这些脚本会自动查找`.egg` 与构建相关的文件，因此，您的 PythonPATH 中可能存在另一个`.egg` 文件干扰该过程。使用以下命令显示 PythonPATH 的内容。
>
>
>      echo $PYTHONPATH
>
> 在类似于`PythonAPI/carla/dist`的路径下查找另一个`.egg`文件，并删除它们。它们可能属于 Carla 安装的其他实例。例如，如果您还通过 *apt-get* 安装了 Carla ，则可以使用以下命令将其删除，并且 PythonPATH 也会被清理。
>
>      sudo apt-get purge carla-simulator
>
> 最终可以选择使用`~/.bashrc`，将PythonPATH下你构建的`.egg`文件添加进来。这不是推荐的方式。最好有一个明确的 PythonPATH，只需在脚本中添加必要的`.egg`文件路径即可。
>
> 首先，打开 `~/.bashrc`.
>
>      gedit ~/.bashrc
>
> 
> 将以下行添加到 `~/.bashrc`。它们存储构建的`.egg`文件路径，以便Python可以自动找到它。保存文件，然后重置终端以使更改生效。
>
> ```
> export PYTHONPATH=$PYTHONPATH:"${CARLA_ROOT}/PythonAPI/carla/dist/$(ls ${CARLA_ROOT}/PythonAPI/carla/dist | grep py3.)"
> export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
> ```
> 
> 清理 PythonPATH 或添加构建的 `.egg`文件路径后，所有示例脚本都应该正常工作。

---

## Windows 构建
<!-- ======================================================================= -->

###### 删除/新建虚拟环境报错：
```shell
# 删除报错
WARNING conda.gateways.disk.delete:unlink_or_rename_to_trash(184): Could not remove or rename C:\software\anaconda3\envs\hutb_3.14\Library\bin\ffi.dll.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.conda_trash.  Please remove this file manually (you may need to reboot to free file handles)
2026-04-29T12:30
...
# 新建报错
[Errno 13] Permission denied: 'C:\\software\\anaconda3\\envs\\hutb_3.14\\Library\\bin\\libbz2.dll'
```

解决：彻底删除虚拟环境。

###### 打包报错：Missing packaged runtime DLLs
```
[Package]: [ERROR] Missing packaged runtime DLLs: AgentInterface.dll dxil.dll embree.2.14.0.dll hdf5.dll libfbxsdk.dll tbb.dll tbbmalloc.dll
[Package]: [ERROR] Required Windows runtime files were not staged.
```
位于：hutb\Build\engine\Engine\Binaries\Win64\AgentInterface.dll (dxil.dll, embree.2.14.0.dll, libfbxsdk.dll, tbb.dll, tbbmalloc.dll)

hutb\Build\engine\Engine\Plugins\Experimental\AlembicImporter\Binaries\Win64\hdf5.dll

解决：[commit](https://github.com/louiszengCN/CarlaAir/commit/2119ed21f65449a9c7857693f1a3cc21dd06e80d) 

###### 'b2' is not recognized as the name of a cmdlet
```
b2 : The term 'b2' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spe
lling of the name, or if a path was included, verify that the path is correct and try again.
At line:1 char:226
+ ... conda3\ ; conda activate hutb; python --version; pip list; b2 -j36 he ...
+                                                                ~~
    + CategoryInfo          : ObjectNotFound: (b2:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
```
解决：设置b2.exe的绝对路径

###### 编译LibCarla报错
```
C:\workspace\hutb\Build\libcarla-visualstudio>cmake -G "Visual Studio 16 2019" -A x64  -DCMAKE_BUILD_TYPE=Server  -DCMAKE_CXX_FLAGS_RELEASE="/MD /MP"  -DCMAKE_INSTALL_PREFIX="C:/workspace/hutb/Unreal/CarlaUE4/Plugins/Carla/CarlaDependencies/"  "C:/workspace/hutb/"
-- Selecting Windows SDK version 10.0.19041.0 to target Windows 10.0.19045.
CMake Error at CMakeLists.txt:4 (include):
  include could not find requested file:

    Build/CMakeLists.txt.in


-- Build debug:   ON
-- Build release: ON
-- Build test:    OFF
CMake Error at LibCarla/cmake/server/CMakeLists.txt:11 (install):
  install FILES given directory "/$Recycle.Bin" to install.


-- Configuring incomplete, errors occurred!
```

分析：安装目录/$Recycle.Bin不存在，表明-DCMAKE_INSTALL_PREFIX="C:/workspace/hutb/Unreal/CarlaUE4/Plugins/Carla/CarlaDependencies/"指向的安装目录不存在，因为前面有模块没有安装成功（一般是boost）。

###### 编译调试模式 LibCarla
```log
  D:\hutb\Unreal\CarlaUE4\Plugins\Carla\Source\Carla/Vehicle/MovementComponents/ChronoMovementComponent.h(21): fatal error C1083: �޷��򿪰����ļ�: ��chrono/physics/ChSystemNSC.h��: No such file or directory
  [2/17] Module.Carla.5_of_5.cpp
  D:\hutb\Build\engine\Engine\Source\Runtime\Core\Public\HAL/Platform.h(1082): note: �μ���TEXT����ǰһ������
  D:\hutb\Unreal\CarlaUE4\Plugins\Carla\Source\Carla\Vehicle\MovementComponents\ChronoMovementComponent.h(21): fatal error C1083: �޷��򿪰����ļ�: ��chrono/physics/ChSystemNSC.h��: No such file or directory
  D:\hutb\Unreal\CarlaUE4\Plugins\Carla\Source\Carla\Vegetation\SpringBasedVegetationComponent.h(22): fatal error C1083: �޷��򿪰����ļ�: ��Eigen/Dense��: No such file or directory
  D:/hutb/Unreal/CarlaUE4/Plugins/CarlaTools/Source/CarlaTools/Private/Online/CustomFileDownloader.cpp(11): fatal error C1083: �޷��򿪰����ļ�: ��OSM2ODR.h��: No such file or directory
```
`Build/*-install` 目录下有，但是`hutb\Unreal\CarlaUE4\Plugins\Carla\CarlaDependencies`目录下没有。


###### 湖工商场景没有生成点
```text
There are no spawn points available in your map/town.
Please add some Vehicle Spawn Point to your UE4 scene.
```

分析：.xodr文件位于：Content\Carla\RoadRunner\Maps\OpenDrive\HutbCarlaCity1.xodr

###### 打包报错：ERROR: System.ArgumentException: Staged filesystem reference may not start with a path separator or contain an empty path fragment (CarlaUE4/Content//Game/roadrunner/map/OpenDrive)

解决：原始的 `DefaultGame.ini`为：
```txt
+DirectoriesToAlwaysStageAsUFS=(Path="/Game/roadrunner/map/OpenDrive")
```
前面不能以`/Game/`开头，直接以目录开头，和`+DirectoriesToAlwaysCook`不同。

##### 打包报错信息：DoesPackageExist FAILED: '/RoadRunnerMaterials/BaseMaterial' is not a standard unreal filename or a long path name. 

```txt
2026-02-28T00:46:51.4815772Z   LogPackageName: Error: DoesPackageExist: DoesPackageExist FAILED: '/RoadRunnerMaterials/BaseMaterial' is not a standard unreal filename or a long path name. Reason: ????????????????'/Engine/', '/Game/', '/Paper2D/', '/AnimationSharing/', '/GeometryMode/', '/Niagara/', '/ChaosSolverPlugin/', '/ChaosClothEditor/', '/SpeedTreeImporter/', '/ChaosNiagara/', '/GeometryCollectionPlugin/', '/GeometryProcessing/', '/DatasmithContent/', '/MotoSynth/', '/PythonScriptPlugin/', '/MediaCompositing/', '/PixelStreaming/', '/AudioSynesthesia/', '/HairStrands/', '/PostSplashScreen/', '/Synthesis/', '/MagicLeap/', '/MagicLeapPassableWorld/', '/SteamVR/', '/AirSim/', '/Carla/', '/CarlaTools/', '/StreetMap/', '/Config/', '/Script/', '/Extra/', '/Memory/', or '/Temp/'??
```
前面还有异常：
```txt
2026-03-01T15:47:46.9162418Z   LogHttp: Warning: 00000231E1AB3900: request failed, libcurl error: 37 (Couldn't read a file:// file)
2026-03-01T15:47:46.9163766Z   LogHttp: Warning: 00000231E1AB3900: libcurl info message cache 0 (Couldn't open file /D:/model1/model1//tileset.json)
2026-03-01T15:47:46.9165181Z   LogHttp: Warning: 00000231E1AB3900: libcurl info message cache 1 (Closing connection -1)
2026-03-01T15:47:46.9267071Z   LogCesium: Error: [2026-03-01 23:47:46.924] [error] [TilesetContentManager.cpp:713] An unexpected error occurs when loading tile: Request failed.
```
原因：中电软件园场景的依赖瓦片`D:/model1/model1//tileset.json`不存在。

原因：`hutb\Unreal\CarlaUE4\Plugins`中未安装RoadRunner插件。


###### 下载 osm2odr 报错：Unknown error (0x80092012) - 吊销功能无法检查证书是否吊销

```shell
# 添加 --ssl-no-revoke 参数
curl --retry 5 --retry-max-time --ssl-no-revoke 120 -L -o OSM2ODR.zip https://github.com/carla-simulator/sumo/archive/%CURRENT_OSM2ODR_COMMIT%.zip
```


###### make PythonAPI报错：“carla/Memory.h”: No such file or directory

将LibCarla\source\carla中的version.h.in重命名为version.h，删除.in文件，然后再次运行make pythonAPI

Version.h.in文件内容
```cpp
// Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

namespace carla {

  constexpr const char *version() {
    return "5966bb718-dirty";
  }

} // namespace carla
```

Version.h文件内容
```cpp
// Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma
// de Barcelona (UAB).
//
// This work is licensed under the terms of the MIT license.
// For a copy, see <https://opensource.org/licenses/MIT>.

#pragma once

namespace carla {

  constexpr const char *version() {
    return "${CARLA_VERSION}";
  }

} // namespace carla
```


###### 在新系统中使用VS2022打开CarlaUE4.sln，提示安装时已经不提供.NET Framework 5.0的目标框架了，打开VS也提示不支持目标框架

> [解决方法](https://www.cnblogs.com/bdqczhl/p/18670152) ：手动加载下载.NET Framework 5.0 框架。


###### 换个用户执行 git 命令时候报错：git config --global --add safe.directory "*"
> ```shell
> git config --global --add safe.directory "*"
> ```


###### pip 安装包时出现 ValueError: check_hostname requires server_hostname 错误

> 关闭代理服务器。

###### 编译 recast 时候报错：Could NOT find SDL2 (missing: SDL2_LIBRARY SDL2_INCLUDE_DIR
  SDL2_SDLMAIN_LIBRARY)
> [解决](https://github.com/carla-simulator/carla/issues/6854#issuecomment-1925019522) ：将 [SDL2-devel-2.30.0-VC.zip](https://github.com/libsdl-org/SDL/releases/download/release-2.30.0/SDL2-devel-2.30.0-VC.zip) 下载并解压到“D:\carla\Build\recast-src\RecastDemo\Contrib”目录下，然后将解压后的文件夹重命名为“SDL”

###### CICD 到 make package 时候出现链接 boost 的错误

> 解决：重新安装报错的 python 虚拟环境。

###### pip install *.whl文件找不到

即使在windows平台下，*.whl文件目录中的分割符需要都是`/`。

###### 执行 xcopy 报 /S 无法识别

解决：原目录和目的目的不能包含 `/` ，需要用`\`替换。

###### BuildCarlaUE4.bat 在jenkins的日志中中文乱码
日志乱码开始出现的地方：
```text
-[BuildCarlaUE4]: Building Unreal Editor...
```

```shell
call "%UE4_ROOT%Engine\Build\BatchFiles\Build.bat"^
    CarlaUE4Editor^
    Win64^
    Development^
    -WaitMutex^
    -FromMsBuild^
    "%ROOT_PATH%Unreal/CarlaUE4/CarlaUE4.uproject"
```



######  添加 SimReady Converter Plugins 后报错：[无法打开包括文件: “WheeledVehicle.h”](无法打开包括文件: “WheeledVehicle.h”)

完整报错信息：`C:\workspace\carla\Unreal\CarlaUE4\Plugins\Carla\Source\Carla\Vehicle/CarlaWheeledVehicle.h(9): fatal error C1083: 无法打开包括文件: “WheeledVehicle.h”: No such file or directory`

解决：关闭 SimReady 插件暂时屏蔽错误，具体 [修改](https://github.com/OpenHUTB/hutb/commit/46bf00b330ab28ae8a6b0181ad848da9f696afd2) 。

###### [使用make PythonAPI编译报错：build\lib.win-amd64-cpython-37\carla\libcarla.cp37-win_amd64.pyd : fatal error LNK1169: 找到一个或多个多重定义的符号](https://github.com/carla-simulator/carla/issues/3621)
出错命令`python setup.py bdist_egg bdist_wheel`。

完整报错信息：
```text
libboost_python37-vc143-mt-x64-1_86.lib(errors.obj) : error LNK2005: "public: static struct boost::python::detail::exception_handler * boost::python::detail::exception_handler::chain" (?chain@exception_handler@detail@python@boost@@2PEAU1234@EA) 已经在 libboost_python37-vc142-mt-x64-1_80.lib(errors.obj) 中定义
libboost_python37-vc143-mt-x64-1_86.lib(errors.obj) : error LNK2005: "private: static struct boost::python::detail::exception_handler * boost::python::detail::exception_handler::tail" (?tail@exception_handler@detail@python@boost@@0PEAU1234@EA) 已经在 libboost_python37-vc142-mt-x64-1_80.lib(errors.obj) 中定义
  正在创建库 build\temp.win-amd64-cpython-37\Release\source/libcarla\libcarla.cp37-win_amd64.lib 和对象 build\temp.win-amd64-cpython-37\Release\source/libcarla\libcarla.cp37-win_amd64.exp
build\lib.win-amd64-cpython-37\carla\libcarla.cp37-win_amd64.pyd : fatal error LNK1169: 找到一个或多个多重定义的符号
error: command 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Tools\\MSVC\\14.44.35207\\bin\\HostX86\\x64\\link.exe' failed with exit code 1169
```
解决：删除`boost-1.86.0-install`和`boost-1.86.0-source`后重新构建，只删除`boost-1.86.0-install`不行。


###### [Chrono库找不到]()
报错信息：
```text
UnrealBuildTool: ERROR: Unhandled exception: Source file 'C:\ProgramData\Jenkins\.jenkins\workspace\carla\Unreal\CarlaUE4\Plugins\Carla\CarlaDependencies\dll\ChronoEngine.dll' does not exist
                        while creating runtime dependencies for module 'Carla'
```
编译目录`Build/chrono-install`目录为空，原因是源代码下载失败。


###### CICD 时找不到.whl文件
报错信息：
```text
(carla_dev) C:\ProgramData\Jenkins\.jenkins\workspace\carla>chcp 65001 
Active code page: 65001
-[Check]: [Batch params]: --smoke
Unreal service is launching with command: start C:\ProgramData\Jenkins\.jenkins\workspace\carla\Build\UE4Carla\v2.0.0-22-g2f520474d\WindowsNoEditor\CarlaUE4.exe -RenderOffscreen ...
The syntax of the command is incorrect.
C:\software\anaconda3\envs\carla_dev\Scripts\pip.exe install --force-reinstall  C:\ProgramData\Jenkins\.jenkins\workspace\carla\Build\UE4Carla\v2.0.0-22-g2f520474d\WindowsNoEditor\PythonAPI\carla\dist\hutb-1.0.0-cp37-cp37m-win_amd64.whl
WARNING: Requirement 'C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\carla\\Build\\UE4Carla\\v2.0.0-22-g2f520474d\\WindowsNoEditor\\PythonAPI\\carla\\dist\\hutb-1.0.0-cp37-cp37m-win_amd64.whl' looks like a filename, but the file does not exist
Processing c:\programdata\jenkins\.jenkins\workspace\carla\build\ue4carla\v2.0.0-22-g2f520474d\windowsnoeditor\pythonapi\carla\dist\hutb-1.0.0-cp37-cp37m-win_amd64.whl
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: 'C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\carla\\Build\\UE4Carla\\v2.0.0-22-g2f520474d\\WindowsNoEditor\\PythonAPI\\carla\\dist\\hutb-1.0.0-cp37-cp37m-win_amd64.whl'
```


###### 升级到vs2022后，编译boost-1.80.0报错：[-[install_boost]: [B2 ERROR] An error ocurred while installing using "b2.exe".](https://github.com/boostorg/boost/issues/914#issuecomment-2327689539)

[解决办法](https://zhuanlan.zhihu.com/p/666616256) ：

执行`b2 install address-model=64 architecture=x86`后删除源代码目录`Build/boost-1.84.0-source`，然后再执行编译就成功（原因不明）。
但是jenkins执行时报错信息包含：
```text
The input line is too long.
The syntax of the command is incorrect.
```
可能因为节点配置的环境路径中递归包含了PATH路径，导致递归输出信息过多，
```shell
http://127.0.0.1:8080/manage/computer/(built-in)/configure
# 键
PATH
# 值
%PATH%;C:\software\GnuWin32\bin;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps;C:\software\anaconda3\condabin;C:\Users\Administrator\AppData\Roaming\npm;C:\software\anaconda3\envs\carla_dev;C:\jenkins\software\Git\bin
```
移除`%PATH%;`即可解决。

第二次执行b2.exe失败，可能是第一步`Build/boost-1.84.0-source`因TortoiseGit删除失败。


1.[删除build，然后将carla文件夹移动到更靠近根目录的位置](https://link.zhihu.com/?target=https%3A//github.com/carla-simulator/carla/discussions/4534)

2.在`Build/boost-1.84.0-source/libs/context/build/Jamfile.v2`里增加以下内容，但并没有修改编译脚本：
```shell
alias asm_sources
   : asm/make_arm_aapcs_elf_gas.S
     asm/jump_arm_aapcs_elf_gas.S
     asm/ontop_arm_aapcs_elf_gas.S
   : <abi>sysv
     <address-model>32
     <architecture>arm
     <binary-format>elf
     <toolset>gcc
   ;
 
alias asm_sources
   : asm/make_arm64_aapcs_elf_gas.S
     asm/jump_arm64_aapcs_elf_gas.S
     asm/ontop_arm64_aapcs_elf_gas.S
   : <abi>sysv
     <address-model>64
     <architecture>arm
     <binary-format>elf
     <toolset>gcc
   ;
```

3.编译命令增加两个选项`address-model=64 architecture=x86`
```shell
b2 install address-model=64 architecture=x86
```

升级boost分析：
> 将 boost 版本从 1.80.0 升级到 1.86.0 可以解决（可以生成lib中的文件）
> 
> 分析过程：
> 
> `.\Util\InstallersWin\install_boost.bat --build-dir "D:\work\workspace\carla\Build" --toolset msvc-14.3 --version 1.80.0 -j 8`报错
> 
> 进入目录`Build\boost-1.80.0-source\`，运行`Build\boost-1.80.0-source\b2.exe address-model=64 architecture=x86`成功

提取出实际运行报错的命令为：
```shell
# 先生成构建文件b2.exe
call bootstrap.bat vc143
# 编译和安装
b2 -j8 headers --layout=versioned --build-dir=.\build    --with-system --with-filesystem --with-python --with-date_time architecture=x86     address-model=64 toolset=msvc-14.3 variant=release link=static runtime-link=shared threading=multi --prefix="D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\boost-1.86.0-install" --libdir="D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\boost-1.86.0-install\lib" --includedir="D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\boost-1.86.0-install" install
```

开发打包编辑器（使用x64 Native Tools可以，但是`call "%PROGRAMFILES%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"` || exit /b 不行）
```shell
%comspec% /k "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && D: && cd D:\work\workspace\carla
call bootstrap.bat vc143
b2 -j24 headers --layout=versioned     --build-dir=.\build    --with-system     --with-filesystem    --with-python     --with-date_time    architecture=x86    address-model=64    toolset=msvc-14.3    variant=release    link=static    runtime-link=shared    threading=multi    --prefix="D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\boost-1.86.0-install"    --libdir="D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\boost-1.86.0-install\lib"    --includedir="D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\boost-1.86.0-install"    install
```

检测到报错是返回值`%errorlevel%`为1，安装的目录中头文件的文件名不对、Lib中的库文件没有生成。

[解读](https://www.bfgroup.xyz/b2/tutorial.html) ：b2 headers ： 生成头文件

`--layout=<layout>`：确定是否选择库名称和头文件位置，以便在同一系统上可以使用多个版本的 Boost 或多个编译器。

    versioned: Boost 二进制文件的名称（libboost_filesystem-vc142-mt-x64-1_80.lib）包含 编译器的名称和版本（vc142）、编码的构建属性（mt：多线程）、Boost 版本号（1_80）。Boost 头文件安装在 <HDRDIR> 的子目录中，该子目录的名称包含 Boost 版本号。

    tagged: Boost 二进制文件的名称包含编码的构建属性，例如变体和线程模型，但不包含编译器名称和版本，也不包含 Boost 版本。如果您使用相同的编译器构建多个 Boost 变体，此选项很有用。

    system: 二进制文件的名称中不包含 Boost 版本号或编译器的名称及版本号。Boost 头文件会直接安装到 <HDRDIR> 目录下。这个选项是专为系统集成商构建的分发包而设计。

    在 Windows 系统中，默认值为“versioned”，而在 Unix 系统中则为“system”。

`--with-system`：需要 system 模块（文件系统操作库）：包括：异常处理、错误码、日志等基础功能；

`--with-filesystem`：需要 [filesystem模块](https://blog.csdn.net/mp553074150/article/details/110734336) ，编译时指定--with-filesystem，包括：类摘要、文件状态、文件属性、文件操作、迭代目录

`--with-python`: 仅编译 python。`b2.exe --show-libraries` 查看 Boost 包含的所有库

`--with-data_time`：处理日期、时间、时间间隔以及与时区相关的操作

`address-model=64`：生成 16 位、32 位或 64 位代码。（可选值为 16, 32, 64, 32_64）

`toolset`: 在条件属性中使用此功能，若某些特性取决于工具集则适用。toolset=msvc:指定 Microsoft Visual C++ (MSVC) 作为编译器工具集，b2会自动检测本地可用的msvc构建器

`variant=release`：variant=debug,release 表示同时编译调试和发布版本

`link=shared`：生成动态链接库 (DLL) 版本的 Boost 库文件,static生成静态库文件。(这里才表示生成静态库)

`runtime-link=shared`：链接到单线程或线程安全的运行时库。（shared, static）

`threading=multi`: 支持多线程的库文件,single生成单线程版本的库文件

```
set PYTHON_ROOT=C:\\Users\\Administrator\\.conda\\envs\\carla_dev\\python.exe
set PYTHON_VERSION=3.7
```


###### [vs2022 下 xerces 编译报错](https://github.com/HARPLab/DReyeVR/issues/86)

报错信息：`error LNK2019: 无法解析的外部符号 u_charType_58，函数 "public: static unsigned short __cdecl xercesc_3_2::XMLUniCharacter::getType(char16_t)"`

```shell
cmake .. -G "Visual Studio 17 2022" -A x64  -DCMAKE_INSTALL_PREFIX="D:/work/workspace/carla/Build/UE4Carla/hutb_editor/carla1/Build/xerces-c-3.2.3-install/"  -DBUILD_SHARED_LIBS=OFF  "D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\xerces-c-3.2.3-source"
```
需要添加`-Dtranscoder=windows`选项：
```shell
cmake .. -G %GENERATOR% %PLATFORM%^
  -DCMAKE_INSTALL_PREFIX="%XERCESC_INSTALL_DIR:\=/%"^
  -DBUILD_SHARED_LIBS=OFF^
  -Dtranscoder=windows^
  "%BUILD_DIR%%XERCESC_BASENAME%-%XERCESC_VERSION%-source"
```

###### [osm2odr报错]()
VS2019升级为2022

```shell
cmake -G "Visual Studio 16 2022" -A x64       -DCMAKE_CXX_FLAGS_RELEASE="/MD /MP"         -DCMAKE_INSTALL_PREFIX="D:/work/workspace/carla/Build/UE4Carla/hutb_editor/carla1/PythonAPI/carla/dependencies/"         -DPROJ_INCLUDE_DIR=D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\\proj-install\include         -DPROJ_LIBRARY=D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\\proj-install\lib\proj.lib         -DXercesC_INCLUDE_DIR=D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\\xerces-c-3.2.3-install\include         -DXercesC_LIBRARY=D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\\xerces-c-3.2.3-install\lib\xerces-c.lib         "D:\work\workspace\carla\Build\UE4Carla\hutb_editor\carla1\Build\osm2odr-source\"
```


###### [boost报错](https://github.com/boostorg/log/issues/113)

报错信息：`carla1\LibCarla\source\carla\FileSystem.cpp(43,14): error C2039: "directory_iterator": 不是 "boost::filesystem" 的成员`，英文：` error C2039: 'directory_iterator': is not a member of 'boost::filesystem'`

解决：[引入丢失的filesystem头文件](https://github.com/boostorg/log/pull/112) 。


###### [make: Nothing to be done for `check'.]()
> Windows.mk中check:标签下一行前面应该是Tab键而不是4个空格。
> check:
> 	 @"${CARLA_BUILD_TOOLS_FOLDER}/Check.bat" --all
> 

###### [使用VS2022 时，make launch 编译 CesiumForUnreal 插件报错](https://stackoverflow.com/questions/3121825/error-c2039-string-is-not-a-member-of-std-header-file-problem)
> 报错信息第一个：`D:\work\workspace\carla\Unreal\CarlaUE4\Plugins\Marketplace\CesiumForUnreal\Source\ThirdParty\include\CesiumGeospatial\S2CellID.h(108): error C2039: "string": 不是 "std" 的成员`
> 
> 解决：头文件中加入：
> 
> `#include <string>`

###### [安装VS2022时出现无法卸载旧版 MSI的错误](https://blog.csdn.net/qq_34988204/article/details/135039621)
> 完整错误信息：错误代码 1714:无法卸载旧版 MSI你的计算机上安装了旧版 MSl。需要先将其卸载才可安装 Visual Studio。
> 
> 快捷键 Win + R 打开运行窗口，输入命令 regedit 并回车，打开注册表编辑器
> 
> 在注册表编辑器中，找到并删除以下注册表项（删除整个Products目录）：
>
> `HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Installer\Products`
> 
> 打开 Visual Studio Installer，点击重试，重新安装 Visual Studio。



###### [编译时卡在：`LogInit: Display: Running engine for game: CarlaUE4`](https://github.com/carla-simulator/carla/discussions/4644)

> 原因：UE找不到GPU spec
> 
> 解决：重启机器。

###### [UnrealBuildTool: ERROR: Unable to instantiate module 'Carla': System.IO.IOException](https://github.com/carla-simulator/carla/discussions/4165)

> 原因：打开依赖项文件夹“carla\Unreal\CarlaUE4\Plugins\Carla\CarlaDependencies”，发现“lib”是一个文件而不是文件夹。
> 
> 解决：删除CarlaDependencies文件夹内的所有文件，并重新编译。

###### [make PythonAPI error "Failed to find XercesC (missing: XercesC_VERSION)"](https://github.com/carla-simulator/carla/issues/5907)

> xerces-c-3.2.3-install 中的头文件目录和库目录是空格，需要删除文件夹，重新编译

###### 从 GitHub 下载时不会出现“CarlaUE4.exe”。 <span id="carlaue4exe-does-not-appear-when-downloading-from-github"></span>

> Carla 的源版本中没有`CarlaUE4.exe`可执行文件。按照构建说明从源代码构建 Carla。要直接获取`CarlaUE4.exe`，请按照 [快速入门](start_quickstart.md) 说明进行操作。

<!-- ======================================================================= -->

###### CarlaUE4 could not be compiled. Try rebuilding it from source manually. <span id="carlaue4-could-not-be-compiled-try-rebuilding-it-from-source-manually"></span>

> 尝试构建 Carla 时出现问题。使用 Visual Studio 重新构建以发现发生了什么。
>
> __1.__ 转到 `carla/Unreal/CarlaUE4` 并右键单击 `CarlaUE4.uproject`。
> 
> __2.__ 单击 __Generate Visual Studio project files__。  
> __3.__ 使用 Visual Studio 2019 打开生成的文件。
> 
> __4.__ 使用 Visual Studio 编译项目。快捷键是F7。构建将失败，但发现的问题将显示在下面。
>
> 不同的问题可能会导致出现此特定错误消息。用户[@tamakoji](https://github.com/tamakoji) 解决了一个经常出现的情况，即源代码未正确克隆且无法设置 Carla 版本（从 git 将其下载为 .zip 时）。
>
> *   __检查 `Build/CMakeLists.txt.in`.__ 如果显示： `set(CARLA_VERSION )`，请执行以下操作： 
>
> __1.__ 转到 `Setup.bat` 第 198 行。 
>
> __2.__ Update the line from: 
> 
> ```
> for /f %%i in ('git describe --tags --dirty --always') do set carla_version=%%i
> ```
> 
> 为：
> 
> ```
> for /f %%i in ('git describe --tags --dirty --always') do set carla_version="0.9.9"
> ```

<!-- ======================================================================= -->

###### 即使 CMake 已正确安装，也会显示 CMake 错误。 <span id="cmake-error-shows-even-though-cmake-is-properly-installed"></span>

> 当尝试使用  _make_ 命令构建服务器或客户端时会出现此问题。即使 CMake 已安装、更新并添加到环境路径中。Visual Studio 版本之间可能存在冲突。
>
> 只留下VS2019，其余的彻底删除。 

<!-- ======================================================================= -->

###### Error C2440, C2672: compiler version. <span id="error-c2440-c2672-compiler-version"></span>

> 由于与其他 Visual Studio 或 Microsoft 编译器版本冲突，该构建未使用 2019 编译器。卸载这些并再次重建。  
>
> Visual Studio 不擅长摆脱自身。要从计算机中彻底清除 Visual Studio，请转到 `Program Files (x86)\Microsoft Visual Studio\Installer\resources\app\layout` 并运行 `.\InstallCleanup.exe -full`。这可能需要管理员权限。  
>
> 要保留其他 Visual Studio 版本，请通过添加以下行进行编辑 ```%appdata%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml``` ： 
>
> ```
>  <VCProjectFileGenerator>
>    <Version>VisualStudio2019</Version>
> </VCProjectFileGenerator>
> ```
> 
> ``` 
>  <WindowsPlatform>
>    <Compiler>VisualStudio2019</Compiler>
> </WindowsPlatform>
> ```  

<!-- ======================================================================= -->

###### “make launch”在 Windows 上不起作用。 <span id="make-launch-is-not-working-on-windows"></span>

> 在构建安装过程中可能会拖出许多不同的问题，并像这样显现出来。以下是最可能的原因列表：
> 
> * __重新启动计算机。__ Windows 构建期间发生了很多事情。重新启动并确保所有内容均已正确更新。
> * __运行虚幻引擎 4.26。__ 构建虚幻引擎时可能出现某些问题。运行编辑器并检查是否使用了 4.26 版本。 
> * __下载资产。__ 如果没有视觉内容，服务器将无法运行。此步骤是强制性的。
> * __Visual Studio 2019.__ 如果安装或最近卸载了其他版本的 Visual Studio，可能会出现冲突。要从计算机中彻底清除 Visual Studio，请转到 `Program Files (x86)\Microsoft Visual Studio\Installer\resources\app\layout` 并运行 `.\InstallCleanup.exe -full`。  
> * __删除 Carla 并再次克隆它。__ 以防万一出了问题。删除 Carla 并重新克隆或下载。
> * __满足系统要求。__ Carla 需要大约 170GB 的磁盘空间和一个专用 GPU（或至少一个 6GB）才能运行。
>
> 系统显示与 HUTB 冲突的其他特定原因可能会发生。请将这些内容发布到 [OpenHUTB 论坛](https://github.com/OpenHUTB/hutb/discussions) 上，以便团队可以更多地了解它们。

<!-- ======================================================================= -->

###### Make 缺少 libintl3.dll 或/和 libiconv2.dll。 <span id="make-is-missing-libintl3dll-orand-libiconv2dll"></span>

> 下载 [依赖项](http://gnuwin32.sourceforge.net/downlinks/make-dep-zip.php) 并将`bin`内容解压到`make`安装路径中。 

<!-- ======================================================================= -->

###### Modules are missing or built with a different engine version. <span id="modules-are-missing-or-built-with-a-different-engine-version"></span>

> 单击 on __Accept__ 以重建它们。

<!-- ======================================================================= -->

###### 尽管成功输出消息，但在`PythonAPI/carla`中没有`dist`文件夹。  <span id="there-is-no-dist-folder-in-pythonapicarla-despite-a-successful-output-message"></span>

> 在 Windows 中， `make PythonAPI` 命令可能会返回一条消息，表明 Python API 安装成功，但实际上并未成功。如果看到此输出后目录 `PythonAPI/carla` 中没有 `dist` 文件夹，请查看上面的命令输出。很可能发生了错误，需要在更正错误并运行 `make clean` 后重试构建。 


###### osm2odr-visualstudio为空，或者拷贝过去的目录不对 <span id="osm2odr_is_null"></span>
```text
CMake Error: The current CMakeCache.txt directory D:/work/workspace/carla/Build/osm2odr-visualstudio/CMakeCache.txt is different than the directory d:/work/buffer/carla/Build/osm2odr-visualstudio where CMakeCache.txt was created. This may result in binaries being created in the wrong place. If you are not sure, reedit the CMakeCache.txt
```
```shell
CMake Error: The source directory "D:/work/workspace/carla/Build/osm2odr-visualstudio/x64" does not appear to contain CMakeLists.txt.
```
> 删除`carla\Build\osm2odr-visualstudio\CMakeCache.txt`


###### 类型转换不对 <span id="type_conversion_error"></span>
> 
```shell
carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vehicle/CustomTerrainPhysicsComponent.cpp(1161): error C2440: “static_cast”: 无法从“float”转换为“EDefResolutionType”
```

> 注释掉
```shell
// ChosenRes = static_cast<EDefResolutionType>(Value);  // static_cast<EDefResolutionType>(Value)
```
注意：注意vs2019专业版才有这个问题，vs2019社区版没有这个问题。

######  链接不到osm2odr.lib <span id="link_osm2odr_failed"></span>
> `fatal error LNK1181: carla\Unreal\CarlaUE4\Plugins\Carla\CarlaDependencies\lib\osm2odr.lib`

> 从其他地方拷贝过来。


######  编译器的堆空间不足 <span id="heap_lack"></span>
> 编译虚幻引擎4时，出现`C1060` 编译器的堆空间不足，说明机器的内存不够，可以参考[链接](https://ue5wiki.com/wiki/32770/) 限制所使用的核心数（默认是使用所有核心数）。
> 修改`Engine/Saved/UnrealBuildTool/BuildConfiguration.xml`中的`MaxProcessorCount`：
```shell
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
  <ParallelExecutor>
    <ProcessorCountMultiplier>7</ProcessorCountMultiplier>
    <MaxProcessorCount>7</MaxProcessorCount>
    <bStopCompilationAfterErrors>true</bStopCompilationAfterErrors>
  </ParallelExecutor>
</Configuration>
```

###### 编译时显示只接受BufferView类型的错误
```text
C:\workspace\carla\Unreal\CarlaUE4\Plugins\Carla\CarlaDependencies\include\carla/streaming/detail/tcp/ServerSession.h(70): error C2338: static_assert failed: 'This function only accepts arguments of type BufferView.'
```
> 拷贝过来的依赖没有更新


* 执行`make PythonAPI`后没有`PythonAPI/carla/dist/`目录

> 报错信息在前面：`CMake Error: Could not create named generator`
> 可能没真正执行命令：`python setup.py bdist_egg bdist_wheel`，需要切换到Python虚拟环境，然后进入`PythonAPI/carla`目录中执行该命令。


* `make PythonAPI` 报 boost 链接的错

报错信息：
```text
libcarla.obj : error LNK2001: 无法解析的外部符号 "void __cdecl boost::python::throw_error_already_set(void)" (?throw_error_already_set@python@boost@@YAXXZ)
...
build\lib.win-amd64-cpython-37\carla\libcarla.cp37-win_amd64.pyd : fatal error LNK1120: 78 个无法解析的外部命令
```
> 问题：使用了多个版本的Python。
> 当您第一次构建 CARLA 时，当它设置 boost 文件时，它会安装一个 Python 版本（如果您有多个版本，它会选择一个您不想要的版本），然后在编译 PythonAPI 时，链接器使用另一个版本的 Python，因此它无法链接不同的版本。
> 
> 因此，请确保默认情况下始终找到相同版本的 Python，并且它是 64 位的。
> 
> 您可以通过查看此处的文件来检查 boost 所使用的 python：
CARLA\Build\boost-1.80.0-install\lib\libboost_python37-vc142-mt-x64-1_80.lib
其中 ..37.. 是 Python 的版本，在本例中为 3.7
> 
> 要重建，只需删除CARLA\Build\boost-1.80.0-install文件夹，然后尝试使用make PythonAPI 再次构建 PythonAPI。
> 参考[链接](https://github.com/carla-simulator/carla/issues/3621) 。

---

## 虚幻引擎

##### 执行打包时报错：ERROR: Unable to find installation of PDBCOPY.EXE, which is required to strip symbols. This tool is included as part of the 'Windows Debugging Tools' component of the Windows 10 SDK (https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk).
> 安装 [Windows Debugging Tools](https://pan.baidu.com/s/1Y0PQeHCMQh7Ln12d_p_Rzw) 后重新编译
> [vs2017](https://download.microsoft.com/download/9/D/2/9D228A37-56C0-48D7-B1B4-486090DE7C2A/vs_Community.exe)

##### UnrealEngine\Engine\Source\Runtime\RenderCore\Private\RenderGraphPrivate.cpp(180): error C4756: 常量算法中溢出
出错代码：`return FLinearColor(INFINITY, INFINITY, INFINITY, INFINITY);`
> 分析：
> 对比新版本SDK的“INFINITY”宏的宏定义：
> 
> 原定义（Windows SDK 10.0.19041.0 所使用）：#define INFINITY ((float)(_HUGE_ENUF * _HUGE_ENUF))
> 
> 新定义：#define INFINITY ((float)(_HUGE_ENF))
> 
> “_HUGE_ENUF”宏并没有改变，这一调整导致了常量算法溢出的问题。
> 
> 原因：Windows SDK 和 MSVC 的版本对源码编译有所影响。
> 
> 添加`UnrealEngine\Engine\Saved\UnrealBuildTool\BuildConfiguration.xml`中指定windows SDK的配置（通过配置手动选择所需版本，参考 [链接](https://blog.csdn.net/qq_41032419/article/details/148902525) ）：
```xml
  <WindowsPlatform>
    <WindowsSdkVersion>10.0.19041.0</WindowsSdkVersion>
  </WindowsPlatform>
```


---

## 打包

### make package 时报错
出错信息：
```shell
LogWindows: Error: begin: stack for UAT
  LogWindows: Error: === Critical error: ===
  LogWindows: Error:
  LogWindows: Error: Fatal error!
  LogWindows: Error:
  LogWindows: Error: Unhandled Exception: EXCEPTION_ACCESS_VIOLATION reading address 0x0000000000000038
  LogWindows: Error:
  LogWindows: Error: [Callstack] 0x00007ffdfaf366c4 UE4Editor-RenderCore.dll!FShaderMapContent::GetOutdatedTypes() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\RenderCore\Private\ShaderMap.cpp:581]
  LogWindows: Error: [Callstack] 0x00007ffd2b4fb28a UE4Editor-Engine.dll!FMaterialShaderMap::GetAllOutdatedTypes() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Engine\Private\Materials\MaterialShader.cpp:1043]
  LogWindows: Error: [Callstack] 0x00007ffd2b983b67 UE4Editor-Engine.dll!GetOutdatedShaderTypes() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Engine\Private\ShaderCompiler\ShaderCompiler.cpp:4216]
  LogWindows: Error: [Callstack] 0x00007ffd2b9a3d03 UE4Editor-Engine.dll!RecompileShadersForRemote() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Engine\Private\ShaderCompiler\ShaderCompiler.cpp:5129]
  LogWindows: Error: [Callstack] 0x00007ffd93651c5d UE4Editor-UnrealEd.dll!UCookOnTheFlyServer::SaveGlobalShaderMapFiles() [D:\work\workspace\UnrealEngine\Engine\Source\Editor\UnrealEd\Private\CookOnTheFlyServer.cpp:5511]
  LogWindows: Error: [Callstack] 0x00007ffd936559dc UE4Editor-UnrealEd.dll!UCookOnTheFlyServer::StartCookByTheBook() [D:\work\workspace\UnrealEngine\Engine\Source\Editor\UnrealEd\Private\CookOnTheFlyServer.cpp:6865]
  LogWindows: Error: [Callstack] 0x00007ffd934943b9 UE4Editor-UnrealEd.dll!UCookCommandlet::CookByTheBook() [D:\work\workspace\UnrealEngine\Engine\Source\Editor\UnrealEd\Private\Commandlets\CookCommandlet.cpp:919]
  LogWindows: Error: [Callstack] 0x00007ffd934be428 UE4Editor-UnrealEd.dll!UCookCommandlet::Main() [D:\work\workspace\UnrealEngine\Engine\Source\Editor\UnrealEd\Private\Commandlets\CookCommandlet.cpp:624]
  LogWindows: Error: [Callstack] 0x00007ff7177896da UE4Editor-Cmd.exe!FEngineLoop::PreInitPostStartupScreen() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Launch\Private\LaunchEngineLoop.cpp:3369]
  LogWindows: Error: [Callstack] 0x00007ff717780e6d UE4Editor-Cmd.exe!GuardedMain() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Launch\Private\Launch.cpp:127]
  LogWindows: Error: [Callstack] 0x00007ff7177811ca UE4Editor-Cmd.exe!GuardedMainWrapper() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Launch\Private\Windows\LaunchWindows.cpp:137]
  LogWindows: Error: [Callstack] 0x00007ff717794e5d UE4Editor-Cmd.exe!WinMain() [D:\work\workspace\UnrealEngine\Engine\Source\Runtime\Launch\Private\Windows\LaunchWindows.cpp:268]
  LogWindows: Error: [Callstack] 0x00007ff717796f02 UE4Editor-Cmd.exe!__scrt_common_main_seh() [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288]
  LogWindows: Error: [Callstack] 0x00007ffe53647374 KERNEL32.DLL!UnknownFunction []
  LogWindows: Error: [Callstack] 0x00007ffe5417cc91 ntdll.dll!UnknownFunction []
  LogWindows: Error:
  LogWindows: Error: end: stack for UAT
Took 232.8404432s to run UE4Editor-Cmd.exe, ExitCode=3
ERROR: Cook failed.
       (see D:\work\workspace\UnrealEngine\Engine\Programs\AutomationTool\Saved\Logs\Log.txt for full exception trace)
AutomationTool exiting with ExitCode=25 (Error_UnknownCookFailure)
卸载 Appdomain 时出错。 (异常来自 HRESULT:0x80131015)
   在 System.AppDomain.Unload(AppDomain domain)
   在 AutomationToolLauncher.Launcher.RunInAppDomain(String[] Arguments) 位置 D:\work\workspace\UnrealEngine\Engine\Source\Programs\AutomationToolLauncher\Launcher.cs:行号 42
BUILD FAILED

-[Package]: [ERROR] There was a problem while packaging Unreal project.
          [ERROR] Please read the screen log for more information.
make: *** [package] 错误 1
```


> [打包分析过程](build/make_package.md)

---

## 运行 Carla
<!-- ======================================================================= -->

###### 运行Carla_0.9.12.sh时候报错：error while loading shared libraries: libomp.so.5。 <span id="load_libraries"></span>

> sudo apt-get install libomp5

<!-- ======================================================================= -->

###### 在虚幻编辑器中运行服务器时 FPS 速率较低。 <span id="low-fps-rate-when-running-the-server-in-unreal-editor"></span>

> 虚幻4编辑器在失焦时会进入低性能模式。  
>
> 转到“编辑->编辑器偏好设置->性能” （`Edit/Editor Preferences/Performance`），然后禁用“处于背景中时占用较少 CPU”选项。

<!-- ======================================================================= -->

###### 无法运行脚本。 <span id="cant-run-a-script"></span>

> 有些脚本有要求。这些列在名为 __Requirements.txt__ 的文件中，与脚本本身位于同一路径中。请务必检查这些以便运行脚本。其中大多数可以通过简单的`pip`命令进行安装。
>
> 有时在 Windows 上，脚本无法仅使用 `> script_name.py` 运行。尝试添加. Try adding `> python3 script_name.py`，并确保位于正确的目录中。

<!-- ======================================================================= -->

###### 在虚幻编辑器中运行时连接到模拟器。 <span id="connect-to-the-simulator-while-running-within-unreal-editor"></span>

> 单击“运行”（ __Play__ ）并等待场景加载。此时，Python 客户端可以像独立模拟器一样连接到模拟器。

<!-- ======================================================================= -->

###### 无法运行 Carla，无论是二进制还是源代码构建。 <span id="cant-run-carla-neither-binary-nor-source-build"></span>

> NVIDIA 驱动程序可能已过时。确保情况并非如此。如果问题仍未解决，请查看 [OpenHUTB 论坛](https://github.com/OpenHUTB/hutb/discussions) 并发布具体问题。

<!-- ======================================================================= -->

###### ImportError: DLL load failed: The specified module could not be found. <span id="importerror-dll-load-failed-the-specified-module-could-not-be-found"></span>

> 所需的库之一尚未正确安装。作为解决方法，请转至 `carla\Build\zlib-source\build`并在脚本的路径中复制名为 `zlib.dll` 的文件。

<!-- ======================================================================= -->

###### ImportError: DLL load failed while importing libcarla: %1 is not a valid Win32 app. <span id="importerror-dll-load-failed-while-importing-libcarla-1-is-not-a-valid-win32-app"></span>

> 32 位 Python 版本在尝试运行脚本时会产生冲突。卸载它并仅保留所需的 Python3 x64。

<!-- ======================================================================= -->

###### ImportError: No module named 'carla' <span id="importerror-no-module-named-carla"></span>

> 出现此错误的原因是 Python 找不到 Carla 库。Carla 库包含在位于`PythonAPI/carla/dist`目录中的一个`.egg`文件中，所有示例脚本都将在此目录中查找它。该`.egg`文件遵循carla-<carla-version>-py<python-version>-<operating-system>.egg 命名法。
>

!!! 重要
    Carla 仅在 0.9.12 之前的版本中使用客户端库文件 `.egg`。如果您使用的是 0.9.12+，有多种方法可以使用/安装客户端库。如果您使用客户端库（`.whl` 或 PyPi 下载）的较新方法之一，本节中的信息将与您无关。

    在 [__快速入门教程__](start_quickstart.md#carla-0912) 中阅读有关使用/安装客户端库的新方法的更多信息。

> 如果您使用的是打包版本的 Carla，则会有多个 `.egg` 文件，对应不同版本的 Python，具体取决于 Carla 的版本。确保您正在使用这些 Python 版本之一运行脚本。要检查默认的 Python 版本，请在命令行中键入以下内容：
>
>
>       python3 --version
>       # 或者
>       python --version 
>

> 如果您从源代码构建 Python，则该`.egg` 文件将根据系统上的默认 Python 版本构建。在 Linux 中，这将是返回的默认 Python 版本：


>       /usr/bin/env python3 --version
>       # 或者如果你指定 ARGS="--python-version=2"
>       /usr/bin/env python2 --version


> 在 Windows 中，它将成为以下功能的默认 Python 版本：

>       py -3 --version

> 确保您使用与您的 `.egg` 文件对应的 Python 版本运行脚本.egg。在 Linux 中，您可能还需要将 Python 路径设置为指向 Carla。为此，请运行以下命令：

>       export PYTHONPATH=$PYTHONPATH:<path/to/carla/>/PythonAPI/carla/dist/<your_egg_file>
>       # 检查现在 Carla 是否能发现
>       python3 -c 'import carla;print("Success")'

> 请注意，虚拟环境或 Conda 等其他 Python 环境可能会使 Carla 的安装变得复杂。确保您已相应地设置 Python 默认值和路径。


###### RuntimeError: rpc::rpc_error during call in function apply_batch <span id="rpc_error"></span>
> PythonAPI的版本要和Carla服务的版本一致，比如dev分支的代码编译得到的虚幻编辑器运行的场景也要用dev分支代码编译的PythonAPI进行连接。


###### ValueError: sticky_control: invalid value type <span id="value_error"></span>
> 客户端和服务端的PythonAPI版本不一致，在dev分支开发时会出现。
> 
> 解决：服务端是dev分支，PythonAPI也要使用在dev分支上编译的客户端。
> 解决2：如果确认Simulator端和客户端版本一致，但是仍然报两者版本不一致的话，先卸载客户端，然后通过`pip install carla`安装官方版本，然后再卸载安装编译版本的*.whl文件即可。

---

## 其他
<!-- ======================================================================= -->

###### 每次打开后都需要进入hutb目录，比较麻烦
> 通过搜索找到`x64 Native Tools Command Prompt for VS 2022`的快捷方式，右键，在`目标(T)`中添加进入目录的参数，成为：
> 
> `%comspec% /k "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && D: && cd D:\work\workspace\carla`


###### Fatal error: 'version.h' has been modified since the precompiled header. <span id="fatal-error-versionh-has-been-modified-since-the-precompiled-header"></span>

> 由于 Linux 更新，这种情况时常发生。Makefile 中有一个针对此问题的特殊目标。虽然花了很长时间，但解决了问题： 
>
>      make hard-clean
>      make CarlaUE4Editor

<!-- ======================================================================= -->

###### 创建 Carla 的二进制版本。 <span id="create-a-binary-version-of-carla"></span>

> 在 Linux 中，在项目文件夹中运行 `make package`。该包将包括项目和 Python API 模块。 
>
> 或者，可以在虚幻编辑器中编译 Carla 的二进制版本。打开 CarlaUE4 项目，转到菜单 `File/Package Project`，然后选择一个平台。可能还要等一下。 

<!-- ======================================================================= -->

###### 我可以在 Linux 计算机上打包适用于 Windows 的 Carla，反之亦然吗？ <span id="can-i-package-carla-for-windows-on-a-linux-machine-and-vice-versa"></span>

>虽然此功能适用于虚幻引擎，但在 Carla 中不可用。我们有许多不支持交叉编译的依赖项。

<!-- ======================================================================= -->
###### 如何卸载 Carla 客户端库？ <span id="how-do-i-uninstall-the-carla-client-library"></span>

>如果您使用 __pip/pip3__ 安装了客户端库，则应通过运行以下命令将其卸载： 

```sh
# Python 3
pip3 uninstall carla

# Python 2
pip uninstall carla
```

---
