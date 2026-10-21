# 虚幻编辑器

* [UE4引擎取消编辑器处于后台时的降帧选项](UE4引擎取消编辑器处于后台时的降帧选项) 
    > Edit -> Editor Preferences -> Miscellaneous，去掉“Use Less Cpu when in Background”复选框上的对号。

* 虚幻编辑器打开后场景是一片灰色，但是场景运行又正常。 
    > 解决：在`世界大纲视图`中选中任意 actor 即可切换到该参与者视角（显示正常）。


* [在编辑器界面运行时候添加运行参数](https://dev.epicgames.com/documentation/unreal-engine/command-line-arguments-in-unreal-engine?lang=zh-CN)
    > 找到 编辑（Edit） > 编辑器偏好设置（Edit > Editor Preferences） 。在左侧，选择 关卡编辑器（Level Editor）> 播放（Play） 。
    > 
    > 在`独立进程游戏中运行`中的`额外启动参数`中添加`--carla-rpc-port=3654`
    > 
    > 注意：不能直接点运行，必须在`独立进程中运行`，否则无效
