# 从源代码构建 Carla

用户可以从源代码构建 Carla 以用于开发目的。如果您想要向 Carla 添加额外的特性或功能，或者想要使用虚幻编辑器创建资源或操作地图，则建议您这样做。

构建说明适用于 Linux 和 Windows。您还可以在 Docker 容器中构建 Carla，以便部署在 AWS、Azure 或 Google 云服务中。访问 [__Carla GitHub__](https://github.com/OpenHUTB/carla) 并克隆存储库。

* [__Linux 构建__](build_linux.md)  
* [__Windows 构建__](build_windows.md)
* [__Docker__](build_docker.md)
* [__带虚幻引擎的 Docker__](build_docker_unreal.md)  
* [__更新 Carla__](build_update.md)  
* [__构建系统__](build_system.md)
* [__在 Linux 上使用虚幻引擎 5.3 构建__](build_linux_ue5.md)  
* [__在 Windows 使用虚幻引擎 5.3 构建__](build_windows_ue5.md)

* [__常见问题__](build_faq.md)  
 

!!! 注意
    这些构建指南都是针对 Carla 的虚幻引擎 4.26 版，如果想要构建基于虚幻 5 的版本（尚不成熟），请访问 [该版本的正确构建指南](https://carla-ue5.readthedocs.io/en/latest/build_carla/) 。



## 其他特性

### 科学上网 <span id="internet"></span>

参考其中的一个链接进行科学上网的订阅和环境配置：[链接1](https://www.starlinkcloud.cc/#/register?code=Ob4iMh8u) 、[链接2](https://stellar.dog/signup?c=vyhcgy)  、[链接3](https://st2.hosbb.com/#/register?code=8l6ICkpN) 。
比如使用Clash，首先在`配置`页面下根据订阅链接进行下载，然后在`常规`页面开启`系统代理`，最后测试是否可以正常科学上网（有些支持在客户端中登录账户即可使用）。并确认代理的端口（比如10090）。

```shell
# 设置代理
git config --global http.proxy 127.0.0.1:10090
git config --global https.proxy 127.0.0.1:10090
# 查看当前的代理设置
git config --global --get http.proxy
git config --global --get https.proxy
# 取消全局代理设置
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### Steamapp 加速

[下载地址](https://steampp.net/) 。定制软件启动的特性：

以下配置文件定位方法已在 Windows 11 25H2、Watt Toolkit（Steam++）3.1.0 上验证。配置文件目录可能与软件安装目录不同，即使软件安装在其他盘，也可以先尝试以下方法。

按 `Win + R`，输入 `cmd` 并按回车，打开命令提示符。分别执行以下命令：


```bat
explorer "%LOCALAPPDATA%\Steam++\Settings"
explorer "%LOCALAPPDATA%\Steam++\Plugins\Accelerator\Settings"
```

第一条命令打开的文件夹中包含 `UISettings.json`，第二条命令打开的文件夹中包含 `ProxySettings.json`。

修改前，请从系统托盘完全退出 Steam++。使用记事本打开原文件，找到下面的字段，只修改对应的值，保留其他内容和原有的行末逗号，不要用示例替换整个文件。

- 默认启动加速页面：

  在 `UISettings.json` 中找到 `StartDefaultPageName`，将其值改为 `"Accelerator-CommunityFix"`：

  ```json
  "StartDefaultPageName": "Accelerator-CommunityFix"
  ```

- 启动软件时默认开启加速：

  在 `ProxySettings.json` 中找到 `ProgramStartupRunProxy`，将其值改为 `true`，注意 `true` 不加引号：

  ```json
  "ProgramStartupRunProxy": true
  ```

保存两个文件后，重新启动 Steam++。不手动切换页面或点击加速按钮，检查软件是否自动进入“网页加速”页面，并自动开启加速。

### Github 访问加速

有时候 Github 访问不了，可以下载并运行 [链接](https://gitee.com/OpenHUTB/sw/releases/tag/up) 中对应平台的软件（比如 Windows 平台中下载 [fastgithub-win-x64.zip](https://gitee.com/OpenHUTB/software/releases/download/speed_up_github/fastgithub-win-x64.zip) 解压后运行`FastGithub.UI.exe`即可正常访问Github）。


其他方法：[链接](https://www.cnblogs.com/ting1/p/18356265) 。

#### Ubuntu 下的配置

Linux 科学上网配置[教程](https://opclash.com/article/302.html) 。下载[clash](https://github.com/zhongfly/Clash-premium-backup/releases/download/2023-09-05-gdcc8d87/clash-linux-amd64-n2023-09-05-gdcc8d87.gz) 。

首次启动`clash`，会新建文件`~/.config/clash/config.yaml`：
```shell
cd $HOME/.config/clash/
```
![ImageDepth](img/build/agent_config.jpg)
将Clash中的订阅地址写入`config.yaml`文件。

打开 Ubuntu 的“设置”管理，在“网络”内将“网络代理”的“自动”改为“手动”，根据以下内容进行填写 HTTP、HTTPS 和 Socks 地址
```shell
# HTTP 代理
127.0.0.1:7890

# HTTPS 代理
127.0.0.1:7890

# Socks 主机
127.0.0.1:7891
```

* stellar
先从[链接2](https://stellar.dog/signup?c=vyhcgy)中注册并下载Ubuntu的客户端
```shell
# 安装客户单
sudo dpkg -i stellar_10.2.2_amd64.deb
# 登录账号后启动代理
```
![](./img/dev/stellar.png)

如果不能正常代理上网，尝试使用全局模式。

#### TortoiseGit 网络代理配置
如果使用TortoiseGit作为git的图形化界面软件，首页在文件资源管理器空白位置右键，选择`TortoiseGit->Setting`，然后在弹出的界面进行如下配置：
![ImageDepth](img/build/internet.jpg)


### [VScode C++开发调式环境配置](https://zhuanlan.zhihu.com/p/679355387)

1.下载`software/gcc/x86_64-8.1.0-release-win32-seh-rt_v6-rev0.7z`文件到本地并解压

2.将`mingw64/bin/`路径添加到PATH路径，使用命令`gcc -v`验证配置已生效；


### 带Carla插件的虚幻编辑器可执行版本

根据 [链接](https://pan.baidu.com/s/1n2fJvWff4pbtMe97GOqtvQ?pwd=hutb) ，CarlaUE4 下载 `software/car/carla_unreal_v1.1.zip`，CarlaUE5 下载 `software/car/CarlaUE5_v1.0.zip`，解压后运行 `launch_*.bat` 就可以启动带Carla插件的虚幻编辑器。

!!! 注意
    CarlaUE5编辑器正常运行至少需要 8GB 显存。


## CI/CD

- [CI/CD环境部署](dev/cicd.md)

- [Applied Intuition的解决方案](https://www.appliedintuition.com/blog/carla-orbis-basis) 

<!--
- 官方CI/CD [链接](http://158.109.8.172:8080/login?from=%2F) （西班牙 加泰罗尼亚的IP）。
-->

