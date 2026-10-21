# [获取 ScenarioRunner](https://github.com/carla-simulator/scenario_runner/blob/master/Docs/getting_scenariorunner.md)

本教程介绍如何下载 ScenarioRunner 并运行一个简单的示例来测试它。ScenarioRunner 需要 Carla 才能运行，并且必须与正在使用的 Carla 版本匹配。如果使用的 Carla 是从源代码构建的，请从源代码下载 ScenarioRunner。如果使用的 Carla 是包，请下载对应版本的ScenarioRunner。

*   __[安装总结](#installation-summary)__  
*   __[A. 下载 ScenarioRunner 发布版](#a.-download-a-scenariorunner-release)__  
	*   [更新发布版](#update-the-release)  
*   __[B. 从源代码下载 ScenarioRunner](#b.-build-scenariorunner-from-source)__  
	*   [从源代码更新构建](#update-the-build-from-source)  
*   __[运行测试](#run-a-test)__  

---
## 安装总结

<details>
   <summary>
    显示快速启动安装的命令行摘要
   </summary>

```sh
# 决定是否使用包或者从源代码构建


# 选项 A) 使用 ScenarioRunner 包
   # 1. 安装 CARLA 包: 
      https://carla.readthedocs.io/en/latest/start_quickstart/
   # 2. 下载匹配的 ScenarioRunner 包: 
      https://github.com/carla-simulator/scenario_runner/releases
   # 3. 抽取内容ntent wherever needed. 

   # Update the release: 
   # 1. Delete previous CARLA and ScenarioRunner versions.
   # 2. Download the latest CARLA release. 
   # 3. Download the matching ScenarioRunner release.


# Option B) Download ScenarioRunner from source
   # 1. Build CARLA from source:
      https://carla.readthedocs.io/en/latest/build_linux/
   # 2. Clone the ScenarioRunner repository: 
git clone https://github.com/carla-simulator/scenario_runner.git
   # 3. Install requirements according to the Python version to be used: 
   # For Python 2.x:
sudo apt remove python-networkx #if installed, remove old version of networkx
pip2 install --user -r requirements.txt
   # For Python 3.x: 
sudo apt remove python3-networkx #if installed, remove old version of networkx
pip3 install --user -r requirements.txt

   # To update ScenarioRunner from source:
   # 1. Update CARLA: 
      https://carla.readthedocs.io/en/latest/build_update/
   # 2. Go to the ScenarioRunner repository, master branch
cd ~/scenario_runner
git branch master
   # 3. Pull the latest changes from the repository
git pull 

```
</details>


---
## A. 下载 ScenarioRunner 发布版

ScenarioRunner 的版本是包含以下内容的软件包： 

*   与特定 CARLA 版本相关的 ScenarioRunner 版本。 

*   用 Python 编写的一些示例场景。 

运行 ScenarioRunner 版本的过程非常简单。  

__1. 下载 CARLA 发布版。__ 请按照 [CARLA 快速入门](https://github.com/carla-simulator/carla/releases) 中的流程进行操作。

__2. 下载匹配的 ScenarioRunner 版本。__ [此处](https://github.com/carla-simulator/scenario_runner/releases) 列出了所有版本。

!!! 重要
    两个版本必须匹配。如果 CARLA 版本是 0.9.9，则还可以使用 ScenarioRunner 0.9.9。[以下](https://github.com/carla-simulator/scenario_runner) 是 CARLA 和 ScenarioRunner 之间的兼容性的简要列表。

__3. 提取内容。__ 目录并不重要。


### 更新发布版

打包版本不需要更新。内容是捆绑的，因此与 CARLA 的特定版本相关联。每次有新的 CARLA 版本时，ScenarioRunner 都会有一个匹配的版本。此处：

*   [CARLA 发布版](https://github.com/carla-simulator/carla/releases)  
*   [Scenario Runner 发布版](https://github.com/carla-simulator/scenario_runner/releases)  

要运行最新版本或任何其他版本，请删除以前的版本并安装所需的版本。

---
## B. 从源代码下载 ScenarioRunner

ScenarioRunner 源存储库包含与最新开发版本 CARLA 一起运行的最具实验性的功能。它不需要构建，因为它只包含 ScenarioRunner 模块的 Python 代码。

__1. 从源代码构建 CARLA。__ 按照文档在 [Linux](https://carla.readthedocs.io/en/latest/build_linux/) 或 [Windows](https://carla.readthedocs.io/en/latest/build_windows/) 上进行构建。

!!! 重要
    ScenarioRunner 需要 CARLA 才能运行，因此文档中规定的 CARLA 最低要求也是运行 ScenarioRunner 所必需的。

__2. 克隆 ScenarioRunner 存储库。__

```sh
git clone https://github.com/carla-simulator/scenario_runner.git
```

__3. 根据要使用的Python版本安装需求。__  首先进入 ScenarioRunner 主目录

```sh
cd ~/scenario_runner/
```

*   __对于 Python 2.x.__  

```sh
sudo apt remove python-networkx #if installed, remove old version of networkx
pip2 install --user -r requirements.txt
```

*   __对于 Python 3.x__  
```sh
sudo apt remove python3-networkx #if installed, remove old version of networkx
pip3 install --user -r requirements.txt
```

!!! 警告
    __不__ 支持高于 v0.8 的 py-tree 。


### 从源代码更新构建

__1. 更新 CARLA 构建__ 按照 [文档](https://carla.readthedocs.io/en/latest/build_update/) 更新 CARLA。

__2. 转到ScenarioRunner 主目录。__ 确保位于本地主分支中。

```sh
cd ~/scenario_runner
git branch master
```
__3. 从存储库中提取最新更改。__  

```sh
git pull
```

__4. 添加环境变量和Python路径__ 这些是系统找到CARLA所必需的，并将PythonAPI添加到Python路径中。

*   __对于 Linux__

```sh
# ${CARLA_ROOT} is the CARLA installation directory
# ${SCENARIO_RUNNER} is the ScenarioRunner installation directory
# <VERSION> is the correct string for the Python version being used
# In a build from source, the .egg files may be in: ${CARLA_ROOT}/PythonAPI/dist/ instead of ${CARLA_ROOT}/PythonAPI
export CARLA_ROOT=/path/to/your/carla/installation
export SCENARIO_RUNNER_ROOT=/path/to/your/scenario/runner/installation
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-<VERSION>.egg
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
```

!!! 注意
    根据注释，使用正确的路径更改命令行。

*   __对于 Windows__


```sh
# %CARLA_ROOT% is the CARLA installation directory
# %SCENARIO_RUNNER% is the ScenarioRunner installation directory
# <VERSION> is the correct string for the Python version being used
# In a build from source, the .egg files may be in: ${CARLA_ROOT}/PythonAPI/dist/ instead of ${CARLA_ROOT}/PythonAPI
set CARLA_ROOT=\path\to\your\carla\installation
set SCENARIO_RUNNER_ROOT=\path\to\your\scenario\runner\installation
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\carla\dist\carla-<VERSION>.egg
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\carla
```

!!! 注意
    根据注释，使用正确的路径更改命令行。

如需永久设置环境变量，请前往 *编辑该账户的环境变量* 。通过在 Windows 的搜索面板上输入 *env* 可以快速访问它。

如果需要运行基于 OpenSCENARIO 2.0 格式的场景，请先安装graphviz和antlr：
```
sudo apt-get install -y openjdk-17-jdk graphviz
curl -O https://www.antlr.org/download/antlr-4.10.1-complete.jar
sudo cp antlr-4.10.1-complete.jar /usr/local/lib/
sudo gedit ~/.bashrc
```
将环境变量添加到~/.bashrc中：
```
export CLASSPATH=".:/usr/local/lib/antlr-4.10.1-complete.jar:$CLASSPATH"
alias antlr4='java -jar /usr/local/lib/antlr-4.10.1-complete.jar'
alias grun='java org.antlr.v4.gui.TestRig'
```
并使更改生效：
```
source ~/.bashrc
```

---
## 运行测试

运行以下车辆示例。首先，您需要从 CARLA 获取最新的主分支。然后您必须将 CARLA Python API [包含到 Python 路径](https://blog.csdn.net/weixin_39910452/article/details/109598890) 中：

!!! 重要
    如果使用源代码构建，请确保上传它们。下载 master 分支中的最新内容。


__1. 运行 CARLA 服务器。__

*   __A) 在从源代码构建中__ ，转到 CARLA 目录并在编辑器中启动服务器。

```sh
cd ~/carla # Change the path accordingly
make launch
# Press Play in the UE Editor
```

*   __B) 在 CARLA 包中__ 直接运行服务器。

```sh
./CarlaUE4.sh
```

__2. 启动示例场景。__ 打开另一个终端，进入ScenarioRunner下载的目录。为了进行本次测试，将使用以下引导车辆场景（`scenario_runner.py`和`manual_control.py`要使用对应的发布版本，开发版不一定成果）。

```sh
# Inside the ScenarioRunner root directory
python scenario_runner.py --scenario FollowLeadingVehicle_1 --reloadWorld
```

使用以下命令查看当前场景有哪些：
```sh
python scenario_runner.py --list
```

!!! 注意
    如果使用 Python 3.x 版本，请运行带有 `python3`. 

__3. 通过手动控制测试场景。__ 打开一个新终端并运行 `manual_control.py`。应该会弹出一个新窗口，街道中央有一辆自主车辆。向前移动，领头车辆就会出现。

```sh
# Inside the ScenarioRunner root directory
python manual_control.py
```

这些场景有大约一分钟的超时时间，以便启动代理。如果出现超时，则应再次启动跟随领先车辆示例。

!!! 警告
    运行`manual_control.py` ScenarioRunner 包/存储库中找到的内容，__而不是 CARLA__ 。 

__4. 探索其他选择。__ 使用 标志运行场景运行器`--help`来探索其他命令行参数和一些基本描述。例如，为了避免自动（重新）加载 CARLA 世界，请跳过命令行选项`--reloadWorld`。 

```sh
python scenario_runner.py --help
```

---

ScenarioRunner 的安装过程至此结束。如果发生任何意外错误或问题，[CARLA 论坛](https://forum.carla.org/c/using-carla/scenario-runner)向所有人开放。有一个ScenarioRunner类别用于发布有关此模块的问题和疑问。

