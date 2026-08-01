# 如何发布

> _本文档适用于想要发布新版本的开发人员。_

!!! 笔记
    已发布的服务：[Carla C++ 文档](https://openhutb.github.io/carla_cpp/dir_b14cdd661f9a7048a44f1771cd402401.html) 、[神经网络原理](https://openhutb.github.io/neuro/) 、[车辆信息可视化内网访问](http://172.21.108.56:8080/) 、[场景像素流](http://172.21.108.56)  、[Jenkins 8080](http://172.21.108.56:8080/) 。

1. **确保内容是最新的。**<br>
   请参阅 [升级内容](tuto_D_contribute_assets.md)。

2. **必要时增加 Carla 版本。**<br>
   增加以下文件中的版本： _DefaultGame.ini_, _Carla.uplugin_,
   _setup.py_, _ContentVersions.txt_ 。Grep 查看当前版本，以确保您不会错过任何参考。

3. **清除 CHANGELOG.md。**<br>
   确保变更日志是最新的，必要时重写并重新组织；考虑哪些项目对用户来说更重要。

4. **提交更改并添加新标签。**<br>
   提交所有更改后，添加一个新标签 `git tag -a X.X.X`
   （用最新版本替换 `X.X.X` ）。 添加此版本的变更日志作为标签消息。

5. **标签内容仓库。**<br>
   在确切的提交处将类似的标签添加到内容存储库，如 _ContentVersions.txt_ 中。

6. **推送更改。**<br>
   将所有更改推送到两个存储库，以推送您可能需要使用
   `git push --tags` 的标签。如有必要，创建拉取请求。

7. **编辑 GitHub 版本。**<br>
   转到 [GitHub 发布](https://github.com/carla-simulator/carla/releases) 并在新创建的标签之上创建一个新版本。等到 Jenkins 完成发布最新版本的构建，并将下载链接添加到新创建的版本。

对应的发布日志位于 [CHANGELOG](changelog.md) 。

## 发布像素流

* [像素流](ue/pixel_streaming.md)

## [下载发行版的可执行程序](./dev/hutb_release.md)




## [发布可执行游戏](https://blog.csdn.net/zl834205311/article/details/125905705) 
* 安装`pyinstaller`：
```shell
pip install pyinstaller
```
或安装图形窗口打包工具：
```shell
pip install auto-py-to-exe
```
然后运行`auto-py-to-exe`。


## 发布带Carla插件的虚幻编辑器

1.参考 [Windows 下的构建](build_windows.md) 进行带Carla插件的虚幻编辑器的构建；

2.发布安装版本
参考[链接](https://github.com/chiefGui/ue-from-source?tab=readme-ov-file#step-by-step-1) 进行虚幻引擎的发布。

3.使用 Visual Studio 打开 `UE4.shn` 。

4.在右侧边栏，您应该会看到一个`解决方案资源管理器`面板。展开`Programs`文件夹并找到`AutomationTool`项目（`Engine\Source\Programs\AutomationTool`）：
![Image](img/ue/AutomationTool.png)

5.右键单击它并选择`生成(Build)`，应该很快。

6.运行安装软件的构建脚本：（如果没有）安装 [Windows 10 SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk) ;

将文件 [`GenerateInstalledBuild.bat`](https://github.com/OpenHUTB/doc/tree/master/src/bat/GenerateInstalledBuild.bat) 拷贝到虚幻引擎源代码的根目录，然后点击运行。

如果一切顺利，您应该会看到`LocalBuilds`与该文件夹处于同一级别的`Engine`文件夹，并且控制台中没有错误。(还包括一个 InstalledDDC 文件夹：DerivedDataCache)。

或者到虚幻引擎源代码主目录中运行下面命令：
```shell
cd Engine\Binaries\DotNET
AutomationTool.exe BuildGraph -target="Make Installed Build Win64" -script=Engine/Build/InstalledEngineBuild.xml -set:HostPlatformOnly=true
```


* 运行``GenerateInstalledBuild.bat`时从报错日志中发现的错误：
```text
ERROR: Visual Studio 2017 must be installed in order to build this target.
```
解决：下载 [链接](https://pan.baidu.com/s/1n2fJvWff4pbtMe97GOqtvQ?pwd=hutb) 的`software/Build Binary`中的 `vs_Community_2017.exe` 或 `3d5_VisualStudio20171509.rar`进行安装。


* 运行``GenerateInstalledBuild.bat`时候报错：
```text
Unable to find installation of PDBCOPY.EXE
```
解决：参考 [链接](https://pan.baidu.com/s/1n2fJvWff4pbtMe97GOqtvQ?pwd=hutb) 的`software/Build Binary`目录 或者 [链接](https://arenas0.com/2018/12/03/UE4_Learn_Build_Binary/) 从 [百度网盘](https://pan.baidu.com/s/1Y0PQeHCMQh7Ln12d_p_Rzw) 下载`X64 Debuggers And Tools-x64_en-us.msi`安装。


* 无法启动
```text
无法启动此程序，因为计算机中丢失XINPUT1_3.dll。尝试重新安装该程
```
解决：参考 [链接](http://www.codefaq.cn/category/Windows/) 安装 DirectX Redist (June 2010)。




## 设计
参考[BeamNG](https://baike.baidu.com/item/BeamNG%E8%B5%9B%E8%BD%A6/18880401)

## 自定义发布

### [发布 hutb PythonAPI到 PyPi](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#uploading-your-project-to-pypi)

1. 注册pypi账号，并激活。

创建一个 PyPI [API 令牌](https://pypi.org/help/#apitoken) ，以便能够安全地上传您的项目。

转到 https://pypi.org/manage/account/#api-tokens 并创建一个新的 API 令牌；不要将其范围限制在特定项目中，因为您正在创建一个新项目。

在复制并保存令牌之前请勿关闭页面 - 您将不会再看到该令牌。

在$HOME/.pypirc文件中加入：
```shell
[pypi]
  username = __token__
  password = pypi-AgEIcHlwaS5*******************
```

2. 生成可发布的whl文件
```shell
make PythonAPI ARGS="--chrono"
```
3. 发布到 [PyPi](https://pypi.org/project/hutb/) ：
```shell
# 删除文件 carla/PythonAPI/carla/dist/hutb-1.0.0-py3.7-win-amd64.egg
pip install twine
twine upload dist/*  # 需要使用PyPi的Token
```
报错：
```text
ERROR    InvalidDistribution: Metadata is missing required fields: Name, Version.
         Make sure the distribution includes the files where those fields are specified, and is using a supported Metadata-Version: 1.0, 1.1, 1.2, 2.0, 2.1, 2.2.
```
检查：
```shell
twine check dist/*
```
通过解压`PythonAPI\carla\dist\hutb-2.2-cp310-cp310-win_amd64.whl`发现：元数据版本`Metadata-Version`为2.4，不在支持的版本之列。

解决：将 3.9~3.13 版本的whl文件用7zip打开，并编辑（F4）`hutb-2.2.dist-info\METADATA`，将`Metadata-Version`改为2.2，然后保存。


___
### pip 连接服务端时自动安装模拟器

```shell
cd hutb\PythonAPI\carla
python setup.py build
# python setup.py install
# 创建一个链接指向你的本地项目目录，修改代码后直接生效，无需重新安装
pip install -e .
# python setup.py develop
# pip install dist\hutb-2.9.16-cp310-cp310-win_amd64.whl
pip uninstall hutb -y
```

```shell
pip show hutb
# 在连接时进行下载
client = carla.Client(args.host, args.port)
# 测试用用例：
python ..\util\config.py -l
```





___

### 发布自定义 mkdocs

* 打包并发布
   ```shell
   git clone https://github.com/OpenHUTB/mkdocs.git
   cd mkdocs
   pip install 'build<0.10.0'
   # 修mkdocs代码改后，将 `mkdocs\__init__.py` 中的版本号+1：
   python -m build
   twine upload dist/*
   # 用户名为`__token__`，密码为token。
   ```

* 开发 hutb-doc
   ```shell
   cd mkdocs
   pip install -e . --force-reinstall
   ```

* 上传提示代理报错：
   ```text
   requests.exceptions.ProxyError: HTTPSConnectionPool(host='upload.pypi.org', port=443): Max retries exceeded with url: /legacy/ (Caused by ProxyError('Unable to connect to proxy', SSLError(SSLZeroReturnError(6, 'TLS/SSL connection has been closed (EOF) (_ssl.c:1149)'))))
   ```
   解决：关闭系统代理即可解决。


* 上传，出现权限不够等错误注意 mkdocs 版本号+1，需要修改 [\_\_init__.py](https://github.com/OpenHUTB/mkdocs/blob/master/mkdocs/__init__.py) 。：
   ```shell
   # 如果报错 requests.exceptions.ChunkedEncodingError: ('Connection broken: IncompleteRead(13780 bytes read, 8681 more expected)', IncompleteRead(13780 bytes read, 8681 more expected))
   twine upload dist/* --repository-url https://pypi.org/project/hutb-doc/
   ```

* 如果出现 twine 命令找不到的问题：`twine : The term 'twine' is not recognized as the name of a cmdlet, function, script file, or operable program.`

   解决：pip 安装解决不了，可以使用本地twine.exe的绝对路径，比如：`C:\Users\Administrator\.conda\envs\ppt2pdf\Scripts\twine.exe upload dist/*`。

   注意：使用 Python 3.7 上传时会报错：
   ```text
   ERROR    InvalidDistribution: Metadata is missing required fields: Name, Version.
         Make sure the distribution includes the files where those fields are specified, and is using a supported
         Metadata-Version: 1.0, 1.1, 1.2, 2.0, 2.1, 2.2.
   ```
  解决：需要使用高版本 Python，比如 Python 3.8.20。


* 使用方法：
   ```shell
   pip install hubt-doc -i https://pypi.org/simple
   ```

* [mkdocs 详细说明](./dev/mkdocs.md)。


### 缩短链接
使用 [tinyurl](https://tinyurl.com/app/my-urls) 缩短文件的长链接，比如 [tinyurl.com/ohutb](tinyurl.com/ohutb) 指向 [carla-0-9-15](https://tiny.carla.org/carla-0-9-15-windows) 。

### 加速页面访问
[cloudflare](https://dash.cloudflare.com/) 全球页面加速访问。



### 发布镜像

* [利用GitHub Actions自动构建项目的docker镜像并发布到DockerHub](https://wiki.eryajf.net/pages/5baf0a/#%E5%89%8D%E8%A8%80)


### 发布到商城
[讨论是否可以发布修改代码的插件](https://www.reddit.com/r/unrealengine/comments/w7ndj9/are_plugins_able_to_append_tooverwrite_engine/)

Baidunet Disk Download Link: https://pan.baidu.com/s/1hFngmeAvyUulsiI-JlNHuA?pwd=hutb

A simulator and scene editor for autonomous driving.

### 发布到gitee

[解决上传出熬过100M大文件的问题](dev/gitee.md) 。


### 发布到 huggingface
```shell
# 添加远程仓库链接
git remote add huggingface https://huggingface.co/datasets/OpenHUTB/Content.git
git push huggingface
# 配置 Token
python -m pip install -U "huggingface_hub[cli]"
huggingface-cli login
```
注意：不能使用用户名密码进行推送，配置Token方法：
```shell
git xet install
git clone https://huggingface.co/datasets/OpenHUTB/hutb
git add hutb.zip
# git lfs ls-files
git commit -m "init"
git remote set-url origin  https://OpenHUTB:<token>@huggingface.co/datasets/OpenHUTB/hutb
# git remote set-url origin https://<user_name>:<token>@huggingface.co/<repo_path>
git push
```

### [发布到微软商城](https://blog.csdn.net/csdn_ad986ad/article/details/135417415)

[**对hutb_downloader.exe进行签名**](https://blog.csdn.net/dounick/article/details/105643285) 。

1. 打开操作系统的 [开发者选项](https://blog.csdn.net/2301_77171572/article/details/146528815) 。

2. 双击安装`.pfx`证书，必须放入`本地计算机`（而不是`当前用户`）的“受信任的根证书颁发机构”，然后选择`将所有的证书都放入下列存储(P)`->`受信任的根证书颁发机构`。

确认 makeappx.exe 是否存在，比如：
```
C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64
```

问题：
```
包 URL 应以 https:// 开头，并且应指向版本控制、可下载的包。
```


* [自签名](https://zhuanlan.zhihu.com/p/29736004658)
* [使用MSIX Packaging Tool工具修改msix程序包](https://www.cnblogs.com/oboth-zl/p/17638705.html)


### 自定义最小化 git



使用 [2.40便携版](https://github.com/git-for-windows/git/releases/download/v2.40.0-rc1.windows.1/PortableGit-2.40.0-rc1-64-bit.7z.exe) 进行瘦身：
测试命令：
```bat
rem 第一次
.\git clone https://OpenHUTB:T8w6TYB_r71gGTP3A02B@git.code.tencent.com/OpenHUTB/lfs_demo.git  &&  cd lfs_demo  && D:\hutb\git\bin\git.exe lfs pull  && cd ..
rem 后面每次
del /q lfs_demo\*.*  && rd /s /q "lfs_demo"  && .\git clone https://OpenHUTB:T8w6TYB_r71gGTP3A02B@git.code.tencent.com/OpenHUTB/lfs_demo.git  &&  cd lfs_demo  && D:\hutb\git\bin\git.exe lfs pull  && cd ..
```
原来有314M，
删除技巧：

1. 一个目录下的dll全部删除，把运行拉取大文件缺少的dll留下；
2. exe文件使用二分法进行删除
3. 其他文本文件尽量全删除

获得的[最小化git](https://gitee.com/OpenHUTB/sw/releases/download/up/git_min.zip) 。


!!! 注意：
   MinGit-2.40.0-rc1-busybox-32-bit.zip 没有git-lfs功能


其他尝试：

下载源码：
```batch
rem 下载
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/git/git/archive/refs/tags/v2.40.3.zip', 'git_v2.40.3.zip')"
rem 解压
powershell -Command "Expand-Archive 'git_v2.40.3.zip' -DestinationPath '.' -Force"
cd git-2.40.3
```

* [包含windows补丁的git](https://github.com/git-for-windows/git/releases) 。

* 安装[Git 的 Windows SDK](https://gitforwindows.org/#download-sdk) ，打开它的 `git-bash.exe`，`cd`进入 Git 的工作树并运行`make`

* git-2.40.0-rc1.windows.1、git-2.41.0.windows.3、git-2.46.0-rc1.windows.1.zip 编译不通过。

* git-2.53.0.windows.2 可以编译通过。

* 使用 PortableGit-2.46.0-rc1-64-bit.7z.exe可以下载大文件


## 问题
点击打包后的文件出现错误：
```text
TypeError: expected str, bytes or os.PathLike object, not _io.BytesIO
```
解决：
```python
pygame.font.Font(pygame.font.get_default_font(), 20)
```
获得的字体文件为`freesansbold.ttf`，最后将字体文件拷贝到和exe文件相同的路径，然后执行即可。

* The following component(s) are required to run this program: Microsoft Visual C++ Runtime

dll所在路径：C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Redist\MSVC\14.44.35112\x64\Microsoft.VC143.CRT\*.dll

解决：vc_redist.x64.exe（位于：C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Redist\MSVC\14.44.35112）
```bat
rem 安装命令
VC_redist.x64.exe /install /quiet /norestart
```

## 参考
* [内网穿透](https://natapp.cn/article/config_ini)
* [元数据检查](https://stackoverflow.com/questions/79791079/twine-error-with-recent-setuptools-build-but-previous-ones-fine-invaliddistribu)