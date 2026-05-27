## 入门示例

!!! 注意
    如果运行 CarlaUE4.exe 时弹出：`Fatal error!`，请从 [Microsoft 网站](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist) 下载 **Microsoft Visual C++ Redistributable** 并安装。在“Visual Studio 2019–2022”下选择 x64 版本。如果运行CarlaUE4.exe时报错：缺少Microsoft Visual C++ Runtime、DirectX Runtime(XINPUT1_3.dll)，则需要分别安装 [vs_community__2019.exe](https://visualstudio.microsoft.com/zh-hans/vs/older-downloads/) （勾选`.NET桌面开发`和`使用C++的桌面开发`）和 [directx_Jun2010_redist.zip](https://www.microsoft.com/zh-CN/download/details.aspx?id=8109)  （解压后运行 [DXSETUP.bat](./DirectX.md) ）。如果发现手动控制车按前进键不能移动，可能是输入法默认是中文，按`Shift`切换成英文输入法即可解决。当机器性能一般时启动`CarlaUE4.exe`报错：`Out of video memory...`，可以通过命令来降低画质启动：`CarlaUE4.exe -quality-level=Low`，以获得更流畅的效果；甚至使用`CarlaUE4.exe -nullrhi`禁用所有渲染（无需 GPU）。



## Python 调用

* `pygame.font.get_fonts()` 运行报错：

复现代码：
```python
import pygame
print(pygame.font.get_fonts())
```

报错信息：
```text
pygame-ce 2.5.7 (SDL 2.32.10, Python 3.10.19)
Traceback (most recent call last):
  File "D:\hutb\Build\bak\test.py", line 3, in <module>
    print(pygame.font.get_fonts())
  File "D:\hutb\Build\dependencies\prerequisites\miniconda3\envs\hutb\lib\site-packages\pygame\sysfont.py", line 520, in get_fonts
    initsysfonts()
  File "D:\hutb\Build\dependencies\prerequisites\miniconda3\envs\hutb\lib\site-packages\pygame\sysfont.py", line 356, in initsysfonts
    fonts = initsysfonts_win32()
  File "D:\hutb\Build\dependencies\prerequisites\miniconda3\envs\hutb\lib\site-packages\pygame\sysfont.py", line 80, in initsysfonts_win32
    if splitext(font)[1].lower() not in OpenType_extensions:
  File "D:\hutb\Build\dependencies\prerequisites\miniconda3\envs\hutb\lib\ntpath.py", line 231, in splitext
    p = os.fspath(p)
TypeError: expected str, bytes or os.PathLike object, not int
```

解决：
1.在 `envs\hutb\lib\site-packages\pygame\sysfont.py` 的 `if splitext(font)[1].lower() not in OpenType_extensions:`之前添加`print(font)`

2.运行`print(pygame.font.get_fonts())`，输出的最后一行即为有问题的字体，比如`1776905345`（不以字体文件为后缀）

3.运行`regedit`打开注册表编辑器，删除包含有问题字体的项，比如`Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Fonts`的`1776905345`在`sdk_init_timestamp`项中。在 Python 中再次运行`pygame.font.get_fonts()`即可解决。

---


* 运行`world.get_blueprint_library()`报错：ValueError: role_name: colors must have 3 channels (R,G,B)

    > 服务端和客户端版本不一致，比如服务端是ue4-dev的最新代码，而客户端为0.9.15的代码。

* 连接不上服务端，又没有报错信息

    > 很可能是因为和 PythonAPI 相关的 [LibCarla 模块](https://github.com/OpenHUTB/hutb/issues/3200#issuecomment-3717221506) 做了更新，而客户端 whl 文件没有更新。


* 运行 Python 程序报错：`Assertion failed: (_data.size() - _offset) % sizeof(T) == 0u, file C:\b\_w\jcarla\jcarla\LibCarla\cmake\..\source\carla/sensor/data/Array.h, line 132`

    原因：由于通过`pip install carla`安装客户端导致import carla混乱。

    解决：
    ```shell
    pip uninstall carla
    pip uninstall hutb
    pip install hutb-2.9.16-cp310-cp310-win_amd64.whl
    ```


## 库的问题
* matplotlib 调用`plt.plot()`报错：`TypeError: int() argument must be a string, a bytes-like object or a number, not 'KeyboardModifier'`

> 将您 Python 升级到 3.8 或者更高、Matplotlib 升级到 3.6.2 或更高版本
> 

## 虚幻编辑器

* RuntimeError: internal error: unable to find spectator

> 运行 UE4 编辑器的模式下，调用 world.get_spectator() 出现这个问题，是因为播放按钮有多种模式，一种是无观察者模式，另一种是有观察者模式。从您发送的截图来看，您运行 UE4 时使用的是 [无观察者模式](https://github.com/carla-simulator/carla/discussions/4782) 。请尝试点击“运行”按钮右边的下拉三角形，选择“独立进程游戏”进行运行（使用另一种模式）。

* 运行场景时弹出`Locate main RenderDoc executable...`选择程序对话框

## 场景

> 解决：下载并安装 图形调试工具 [renderdoc](https://renderdoc.org/) ，然后在选择程序对话框中选择`C:\Program Files\RenderDoc\qrenderdoc.exe`。

# 崩溃

运行CarlaUE4.exe报错：
```shell
The UE4-CarlaUE4 Game has crashed and will close
LowLevelFatalError [File:Unknown] [Line: 136]Exception thrown: bind: ??h????E???????k?"????h???????-????m? [system 10013 atD:/carla unreal/carla/Build/boost-1.80.0-install/include\boost/asio/detail/win_iocp_socket_service.hpp:244:5 in function 'bind']
```
> 原因：本地端口被其他程序占用。
>
> 解决：重启电脑


## 其他

[__构建问题__](../build_faq.md) — 解决构建代码时候最常见的问题

[__虚幻引擎问题__](../ue/ue_faq.md) - 虚幻引擎的一些专业问题
