## 像素流推送

### 步骤
参考 [像素流送入门](https://openhutb.github.io/engine_doc/zh-CN/SharingAndReleasing/PixelStreaming/PixelStreamingIntro/index.html) 进行配置：

1. 打开像素流插件；
2. 在主菜单中选择 编辑（Edit） > 编辑器偏好（Editor Preferences...）。然后在 关卡编辑器（Level Editor） > 播放（Play） 中找到 额外启动参数（Additional Launch Parameters） 设置，并将其值设为 `-AudioMixer -PixelStreamingIP=localhost -PixelStreamingPort=8888`。
3. 按住 Alt 键并拖动 .exe 文件即可在相同文件夹中（或在其他任意处）新建一个快捷方式。右键点击快捷方式并从上下文菜单中选择 属性（Properties）。在 *快捷方式属性（Shortcut Properties） 窗口的 快捷方式（Shortcut） 选项卡中，在 目标（Target） 域的末尾附加文本 `-AudioMixer -PixelStreamingIP=localhost -PixelStreamingPort=8888 -RenderOffScreen` 并点击 确认**。
4. 启动`CarlaUE4.exe`，从[链接](https://nodejs.org/zh-cn/download) 下载并安装node.js，然后启动像素流的信令服务`run.bat`；
5. 使用浏览器访问 [http://127.0.0.1/](http://127.0.0.1/) 测试是否能够访问到像素流。

**CarlaUE4.exe 启动的后缀命令说明**

* -AudioMixed

将声音加入像素流送中

* -AllowPixelStreamingCommands

允许用emitcommand发送 UE4控制台命令

* -PixelStreamingIP=localhost

像素流送IP地址

* -PixelStreamingPort=8888

像素流送端口

* -RenderOffScreen

在后台运行游戏程序实例

* -log

运行游戏程序实例过程中打印log

* -NvEncH264ConfigLevel=NV_ENC_LEVEL_H264_52

高分辨率必须添加本参数，否则会报nv错误

* -ResX=1920  -ResY=1080

设定分辨率


### 优化

量化参数（Quantization Parameter, QP）值用于控制每帧视频中每一个宏块的压缩量，和比特率成反比，QP值越小画质越高。

### 打开页面自动播放

webRtcPlayer.js 的53行添加
```shell
video.autoplay = true;
video.muted = true;
```
同时隐藏按钮：player.css中修改`#videoMessageOverlay`和`#videoPlayOverlay`的`z-index`属性为`-1`。

### 问题
> 使用链接`http://127.0.0.1:8888`访问时出现：`Upgrade Required`，改用地址`http://127.0.0.1:80`访问则没有问题。

>  当启动信令服务后访问不了像素流（出现：Disconnected: Streamer is not connected），尝试关闭系统代理然后再访问。

排查`netstat -ano|findstr “8888”`端口是否被占用

出现`Streamer connected: ::1`才表示像素流正常工作。

> - 页面中点击开始后，出现`Fatal error!`的错误。命令行同时出现`streamer disconnected: 4000 - Failed to parse answer's SDP`的错误。
> 
> 解决：参考 [链接](https://zhuanlan.zhihu.com/p/383825174) ，或者复制 [gpt](https://github.com/OpenHUTB/gpt) 中的文件替换，即：
> 
> 在`Engine/Source/Programs/PixelStreaming/WebServers/SignallingWebServer/scripts/webRtcPlayer.js`于61行添加：
> ```
> this.cfg.offerExtmapAllowMixed = false;
> ``` 
> 第125行添加下行代码：
> ```shell
> offer.sdp = offer.sdp.replace(/(a=extmap-allow-mixed)\r\n/gm, "");
> ```

### 参考

- [交通大模型实现的像素流推送](https://github.com/OpenHUTB/gpt/tree/main/sim/WindowsNoEditor/Engine/Source/Programs/PixelStreaming/WebServers/SignallingWebServer)
- [像素流送入门](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/getting-started-with-pixel-streaming?application_version=4.27)
- [流送优化指南](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/stream-tuning-guide)
