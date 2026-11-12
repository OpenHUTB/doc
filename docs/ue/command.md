# # 命令行操作

在运行场景时按重音键 ` （键盘右上角，Esc 下的那个键），调出命令行窗口，再次按下关闭。
输入命令时会有自动补全提示，按 Tab 补全，按 ↑ 调出历史命令。

模拟器基于 Unreal Engine 4.26，引擎自带一套控制台命令，可在运行时调整画质、查看性能、控制时间，
无需重启模拟器。本文列出仿真中常用的命令，完整列表见文末参考链接。

!!! note
    部分命令在打包发布版（Shipping/Test）中可能被裁剪，以实际运行时的补全提示为准。

## 编辑器常用操作

| 作用                                        | 操作                                                                                                                                 |
|-------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| 让引擎右上角一直显示帧率 和 内存使用情况    | 勾选“编辑器偏好设置 Editor Preferences”> 通用-性能（Performance）> 显示帧率和内存（Show Frame Rate and Memory）   |
| 显示各种GPU上的消耗细则   | `show stats`（Shift+L） |
| profile GPU 显示当前状态GPU消耗   | Ctrl + Shift + , （逗号） |
| 进入Debug Mode（循环切换：Debug+Controls、物理状态）   | 按F8（控制：连接到玩家控制器）后按 `;` （分号键） |
| 聚焦选定的角色（摄像机对齐）   |在编辑器中选中参与者，按 F 键 |
| 将编辑器摄像机移动到特定位置并旋转   | `bugitgo 0 0 0 0 0 0` 会将摄像机移动到世界坐标 (0, 0, 0)，旋转角度为 (0, 0, 0) |

## 性能统计

| 命令 | 作用 |
|:-----|:-----|
| `stat fps` | 显示当前帧率（相当于快捷键 Ctrl+Shift+H） |
| `stat unit` | 显示帧耗时分解（Game / Draw / GPU） |
| `stat rhi` | 显示 RHI 层的 Draw Call / CPU 消耗 |
| `stat unitgraph` | 以曲线图显示帧耗时 |
| `stat game` | 显示游戏线程耗时明细 |
| `stat scenerendering` | 显示渲染线程耗时明细 |
| `stat memory` | 显示内存占用 |
| `stat physics` | 显示物理计算耗时 |
| `stat none` | 关闭所有统计信息 |

## 帧率与分辨率

| 命令 | 作用 |
|:-----|:-----|
| `t.MaxFPS 30` | 限制最大帧率为 30（`0` 表示不限制） |
| `r.VSync 1` | 开启垂直同步（`0` 关闭） |
| `r.ScreenPercentage 50` | 按屏幕百分比渲染，用于降低 GPU 负载 |
| `r.SetRes 1280x720` | 设置渲染分辨率（加 `w` 后缀为窗口模式，`f` 为全屏） |

## 画质等级

`sg` 系列命令按 0–3 调整画质，0 为最低、3 为最高（Epic）：

| 命令 | 作用 |
|:-----|:-----|
| `sg.ViewDistanceQuality 1` | 视距 |
| `sg.AntiAliasingQuality 1` | 抗锯齿 |
| `sg.ShadowQuality 1` | 阴影 |
| `sg.PostProcessQuality 1` | 后处理 |
| `sg.TextureQuality 1` | 贴图 |
| `sg.EffectsQuality 1` | 特效 |
| `sg.FoliageQuality 1` | 植被 |

## 显示开关

`showflag` 系列命令按 0/1 关闭或开启某类渲染内容，常用于排查渲染问题或提升性能：

| 命令 | 作用 |
|:-----|:-----|
| `showflag.PostProcessing 0` | 关闭后处理 |
| `showflag.Shadows 0` | 关闭阴影 |
| `showflag.Decals 0` | 关闭贴花 |
| `showflag.Particles 0` | 关闭粒子 |
| `showflag.Fog 0` | 关闭雾效 |
| `showflag.SkyLighting 0` | 关闭天光 |

## 时间与场景

| 命令 | 作用 |
|:-----|:-----|
| `slomo 0.5` | 时间缩放，`0.5` 为半速，`2` 为两倍速 |
| `slomo 1` | 恢复正常速度 |
| `pause` | 暂停/继续 |
| `open Town10HD` | 在编辑器中切换到指定地图 |
| `quit` | 退出模拟器 |

## 启动参数

以下参数在启动可执行文件时传入，效果同控制台命令，适合写进脚本：

```shell
# 窗口模式，分辨率 1280x720
CarlaUE4.exe -windowed -ResX=1280 -ResY=720

# 画质等级
CarlaUE4.exe -quality-level=Low

# 固定帧率基准测试
CarlaUE4.exe -benchmark -fps=20
```

## 参考

- Unreal Engine 4 控制台命令完整列表：<https://framedsc.com/GeneralGuides/ue4_commands.htm>
- Unreal Engine 官方文档 - Console Commands：<https://docs.unrealengine.com/4.26/en-US/ProductionPipelines/ConsoleCommands/>


