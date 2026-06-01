# <p align=center> 开源孪创  </p>

<!-- Badges (flat): https://github.com/pudding0503/github-badge-collection -->
<p align=center>
    <a href="https://github.com/OpenHUTB/doc/actions">
        <img src="https://raw.githubusercontent.com/OpenHUTB/doc/refs/heads/master/docs/img/badge.svg" alt="Continuous Integration Badge">
    </a>
    <a href="https://github.com/OpenHUTB/doc/releases">
        <img src="https://img.shields.io/github/v/release/OpenHUTB/doc" alt="Releases Badge">
    </a>
    <a href="https://github.com/OpenHUTB/doc/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License Badge">
    </a>
    <a href="https://github.com/OpenHUTB/doc">
        <img src="https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey" alt="Supported Platforms Badge">
    </a>
    <a href="https://zenhub.com">
        <img src="https://img.shields.io/badge/Shipping%20faster%20with-ZenHub-blueviolet" alt="ZenHub Badge">
    </a>
    <a href="https://github.com/OpenHUTB/doc/graphs/contributors">
        <img src="https://img.shields.io/github/contributors/OpenHUTB/doc" alt="ZenHub Badge">
    </a>
    <a href="https://github.com/OpenHUTB/doc">
        <img src="https://img.shields.io/github/forks/OpenHUTB/doc" alt="ZenHub Badge">
    </a>
</p>

该项目是一款能让用户快速测试 [具身人](https://openhutb.github.io/doc/#_5) 、[无人车](https://openhutb.github.io/doc/#_4) 、[无人机](https://openhutb.github.io/air_doc/) 感知、规划、控制算法的影视级物理模拟器文档。

<p width="100%" display="flex" align="center">
<a href="https://openhutb.github.io/doc/tuto_G_pedestrian_navigation/#conclusion"><img src="docs/img/pedestrian/cycle.gif" width="27%" margin-right="10%"/></a>  <a href="https://openhutb.github.io/doc/tuto_G_chrono/"><img src="https://github.com/OpenHUTB/chrono_doc/blob/master/docs/img/chrono/vechile_turnover.gif?raw=true" width="30%"/></a> <a href="https://openhutb.github.io/air_doc/"><img src="https://github.com/OpenHUTB/air_doc/blob/master/docs/images/dev/HUTB_simulation.gif?raw=true" width="30%"/></a>
</p>

---

## 文档部署

1. 安装 python 3.11+，使用`pip`安装`mkdocs`
```shell
# 只克隆主分支
git clone -b master --single-branch https://github.com/OpenHUTB/doc
# 安装依赖
conda create -n mkdocs python=3.11
conda activate mkdocs
pip install git+https://github.com/OpenHUTB/mkdocs.git
pip install -r requirements.txt
```
（可选）安装完成后使用`mkdocs --version`查看是否安装成功。

2. 在命令行中进入`doc`目录下，运行：
```shell
# 构建文档（根据Markdown文件生成HTML文件）
# mkdocs build
# 启动服务
mkdocs serve
```
然后使用浏览器打开 [http://127.0.0.1:8000](http://127.0.0.1:8000)，查看文档页面能否正常显示。

3. 部署到`github`（可选，需要仓库的写入权限）：
```shell
mkdocs gh-deploy
```
该命令会自动将相应内容推送到项目的`gh-pages`分支上，然后在 `Github` 项目设置中选择好对应 `GitPage` 的分支，目录选择`/(root)`（注意不要是`/(docs)`，然后通过 [`https://openhutb.github.io/doc/`](https://openhutb.github.io/doc/) 访问即可。

使用虚拟环境会出现找不到`git`的错误，请添加`git`的环境变量：
```shell
set path=%path%;C:\Program Files\Git\cmd\
```

4. 删除页脚（可选）
* 克隆删除页脚的mkdocs仓库（删除`mkdocs/themes/readthedocs
/footer.html`文件中的页脚内容）：
```shell
git clone https://github.com/OpenHUTB/mkdocs.git
```
安装mkdocs包：
```shell
cd mkdocs
# 可编辑（--editable）模式安装，本地修改 mkdocs 代码后，需要重启 mkdocs serve 才会生效
python -m pip install -e .
# 或者安装发布模式
# python -m pip install . -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```
然后使用新的 mkdocs 执行步骤 1-3。

注意：发布自定义 mkdocs 请参考 [链接](https://openhutb.github.io/doc/tuto_D_make_release/) 。


## 软件发布
将源代码、文档、软件等进行发布，具体步骤参考 [链接](publish.md) 。


## 撰写规范

### 命名规则

`adv_*.md (advise_*.md)` : 建议

`build_*.md` : 源代码构建

`tuto_A_*.md (tutorial_asset_*)` : 资产教程

`tuto_D_*.md (tutorial_development_*)` : 开发教程

`tuto_E_*.md (tutorial_example_*)` : 参考示例

`tuto_G_*.md (tutorial_guide_*)` : 指南教程

`tuto_M_*.md (tutorial_map_*)` : 地图教程

- 页面跳转
1. 定义一个锚(id)： `<span id="jump"></span>` 或 `<span id="jump">跳转到的地方</span>`
2. 使用 markdown 语法：`[点击跳转](#jump)`


### 颜色规范

橙色的变量名 **<font color="#f8805a">variable</font>**：
```shell
**<font color="#f8805a">variable</font>**
```
绿色的方法名 **<font color="#7fb800">method</font>** ：
```shell
**<font color="#7fb800">method</font>**
```
蓝色的函数参数名 **<font color="#00a6ed">self</font>** ：
```shell
**<font color="#00a6ed">self</font>**
```
红色的 <font color="#ED2F2F"> 警告 </font>
```shell
**警告：** <font color="#ED2F2F">_ hutb_</font>
```

### 公式

注意：`markdown_extensions:`标签内需要加上`- mdx_math`（python环境需要安装依赖`python-markdown-math`）。

行内公式
```text
\(...\)
```


行间公式
```text
$$
a + b = c
$$
```

### 链接

鼠标停留在链接上显示提示文字
```shell
[正文](链接 "浮现文字")
```

### 多媒体展示

常见图的绘制请参考[绘图指南](docs/demo/figure.md) 。


文档页面显示支持 [Latex 公式](https://gist.github.com/josemazo/36af7bb9c58b92c684bbd431f6c68ce9) 、[视频播放](https://pypi.org/project/mkdocs-video/)  。


### 其他

* mkdocs 定制

    修改完 [mkdocs](https://github.com/OpenHUTB/mkdocs) 仓库后，使用以下命令进行**本地安装**：
    ```shell
    pip uninstall mkdocs -y
    cd mkdocs
    python -m pip install .
    ```
    由于 **Github Action** 的 [OpenHUTB/actions-mkdocs](https://github.com/Tiryoh/actions-mkdocs/compare/main...OpenHUTB:actions-mkdocs:main) 需要使用 `pip install hutb-doc -i https://pypi.org/simple` 进行安装，所以需要先删除 [pypi 已发布的包](https://pypi.org/manage/project/hutb-doc/releases/) ，然后再参考 [发布自定义mkdocs](https://openhutb.github.io/doc/tuto_D_make_release/) 发布 hutb-doc。

* [将 deepwiki 页面下载为 markdown 格式](https://zhuanlan.zhihu.com/p/1903904027554604441)

    [下载](https://github.com/philipz/deepwiki-md-chrome-extension/releases)并解压插件 -> 在 Chrome 浏览器中的地址栏中输入`chrome://extensions`打开开发模式 -> 点击`加载未打包的扩展程序`，选择刚才下载来的根目录 -> 点击增加的扩展程序的`详情`按钮启用`自动访问deepwiki`和`固定到工具栏` -> 打开对应的 deepwiki 页面，点击工具栏中的新出现的按钮，选择`Download Current Page`。


## 常见问题

* 修改文件后不自动加载更新

    > 解决：将 click 的版本从 8.3.0 回退到 8.2.1
    > 
    > `pip install  --force-reinstall click==8.2.1`
    >
    > 或者使用以下命令启动服务：`mkdocs serve --livereload`

* 编译文档时报错：`ERROR - Config value: ‘plugins‘. Error: The “redirects“ plugin is not installed`

  > [解决](https://blog.csdn.net/LostSpeed/article/details/127192365) ：
  > ```shell
  > pip install redirects
  > ```


* 编译文档时报错：`Config value: 'markdown_extensions'. Error: Failed loading extension "mdx_gh_links".`
  > 解决：[手动安装库](https://github.com/mkdocs/mkdocs/issues/1587) ：
  > ```shell
  > pip install mdx_gh_links
  > ```

* 克隆仓库时报错：`fatal: fetch-pack: invalid index-pack output`
  > 解决：
  > ```shell
  > # 设置下载缓存参数
  > git config --global http.postBuffer 2G
  > # 确认参数是否正确设置
  > git config http.postBuffer
  > ```

* 安装完 hutb-doc 后，运行`mkdocs serve --livereload`报错：ModuleNotFoundError: No module named 'pymdownx'
    > 解决：
    > ```shell
    > pip install pymdown-extensions
    > ```

## 许可证

```
@inproceedings{airsim2017fsr,
  author = {Shital Shah and Debadeepta Dey and Chris Lovett and Ashish Kapoor},
  title = {AirSim: High-Fidelity Visual and Physical Simulation for Autonomous Vehicles},
  year = {2017},
  booktitle = {Field and Service Robotics},
  eprint = {arXiv:1705.05065},
  url = {https://arxiv.org/abs/1705.05065}
}
```

```
@article{sture,
	author={Haidong Wang and Zhiyong Li and Yaping Li and Ke Nai and Ming Wen},
	title={STURE: Spatial-Temporal Mutual Representation Learning for Robust Data Association in Online Multi-Object Tracking},
    journal={Computer Vision and Image Understanding},
	volume=220,
	year=2022,
}
```

此项目依据 MIT 许可证发布。详情请查阅[许可证文件](./LICENSE)。