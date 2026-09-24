#   提取 DirectX 的 DLL 文件

1. 运行“directx_Jun2010_redist.exe”文件，并接受许可协议。

2. 请注明包内物品将被提取至的目的地。——例如：D:\DX9 。

3. 可重分布软件包的内容现已被解压至 D:\DX9 文件夹中。

4. 您可以手动从每个 CAB 文件中提取文件，但这种方式很繁琐。建议您使用“Expand.exe”命令行工具来操作。

在“DX9”文件夹中，输入“cmd.exe”进入地址栏。这样就会在该文件夹中打开一个命令提示窗口。

5. 在命令提示符窗口中，请执行以下操作：

```shell
# 新建目录
md Files\x64
md Files\x86
# 提取文件到新建的目录中
expand.exe -r *x86.cab -F:*.DLL .\Files\x86
expand.exe -r *x64.cab -F:*.DLL .\Files\x64

```

现在，这些动态链接库已被提取到“D:\DX9\Files\x86”和“D:\DX9\Files\x64”这两个目录中。


如果您的游戏软件提示缺少 DirectX 9-10 运行环境，请按照以下步骤操作：

**在 64 位 Windows 系统中**：

将相应的文件从“x64”文件夹复制到“C:\Windows\System32”文件夹。

将相应的文件从“x86”文件夹复制到“C:\Windows\SysWOW64”文件夹。


**在 32 位 Windows 系统中**：

将相应的文件从“x86”文件夹复制到“C:\Windows\System32”文件夹中。

重要提示：在 64 位 Windows 系统安装中，请勿将 32 位的动态链接库复制到“Windows\System32”文件夹中。这样做会导致各种应用程序出现错误。请将所需的 32 位模块复制到“Windows\SysWOW64”文件夹中。

（若要确认您的 Windows 系统是 32 位还是 64 位，请使用本文中所提供的方法之一：《查找您的 Windows 版本、系列及位数》。）

## 解决方法

下载 [DirectX_Runtime.zip](https://gitee.com/OpenHUTB/sw/releases/download/up/DirectX_Runtime.zip) 并解压到本地，如果是x64操作系统，就将x64目录下的所有dll文件拷贝到 CarlaUE4\Binaries\Win64 目录 、或者 Engine\Binaries\Win64目录（没有可以新建）、或者 和CarlaUE4.exe 相同的文件夹中，如果是x86则是类似的操作。


## 参考

* [如何从 DirectX（2010 年 6 月版）运行时安装程序中提取 DLL 文件](https://www.winhelponline.com/blog/directx-end-user-runtime-dll-files/)

* [【UE4】使用动态库(DLL)提示找不到dll的解决方案](https://zhuanlan.zhihu.com/p/556830150)
